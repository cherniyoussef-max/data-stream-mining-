"""Replace static posters with embedded animated GIF media, retaining slide geometry."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import posixpath
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

from PIL import Image


P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CT = "{http://schemas.openxmlformats.org/package/2006/content-types}"


def build(poster, target):
    slides = json.loads(Path("presentation/slides.json").read_text(encoding="utf-8"))
    root = Path("presentation/animations")
    with ZipFile(poster) as source:
        content = {name: source.read(name) for name in source.namelist()}
    types = ET.fromstring(content["[Content_Types].xml"])
    if not any(node.get("Extension") == "gif" for node in types):
        ET.SubElement(types, CT+"Default", {"Extension":"gif","ContentType":"image/gif"})
    ET.register_namespace("",CT[1:-1])
    content["[Content_Types].xml"] = ET.tostring(types, encoding="utf-8", xml_declaration=True)
    ET.register_namespace("",REL[1:-1])
    for row in slides:
        if not (key := row.get("anim")):
            continue
        n = row["number"]
        s = ET.fromstring(content[f"ppt/slides/slide{n}.xml"])
        pictures = s.findall(".//"+P+"pic")
        assert len(pictures) == 1
        blip = pictures[0].find(".//"+A+"blip")
        relation_id = blip.get(R+"embed")
        relations_path = f"ppt/slides/_rels/slide{n}.xml.rels"
        relations = ET.fromstring(content[relations_path])
        node = next(node for node in relations if node.get("Id") == relation_id)
        assert node.get("Type").endswith("/image")
        old_media = node.get("Target").lstrip("/")
        assert old_media in content
        assert sha256(content[old_media]).digest() == sha256((root/f"{key}.png").read_bytes()).digest()
        asset = f"ppt/media/project4-{key}.gif"
        content[asset] = (root/f"{key}.gif").read_bytes()
        node.set("Target", "../media/"+posixpath.basename(asset))
        content[relations_path] = ET.tostring(relations, encoding="utf-8", xml_declaration=True)
    with ZipFile(target, "w", compression=ZIP_DEFLATED) as out:
        for name, data in content.items():
            out.writestr(name, data)
    return slides


def validate(path, rows):
    animations = []
    with ZipFile(path) as deck:
        assert deck.testzip() is None
        members = set(deck.namelist())
        notes = sum(bool(re.fullmatch(r"ppt/notesSlides/notesSlide\d+.xml",name)) for name in members)
        timing, transitions, video = 0, 0, 0
        for row in rows:
            n = row["number"]
            slide = ET.fromstring(deck.read(f"ppt/slides/slide{n}.xml"))
            timing += slide.find(P+"timing") is not None
            transitions += slide.find(P+"transition") is not None
            video += len(slide.findall(".//"+A+"videoFile"))
            if not (key := row.get("anim")):
                continue
            rels = ET.fromstring(deck.read(f"ppt/slides/_rels/slide{n}.xml.rels"))
            relationship_id = slide.find(".//"+A+"blip").get(R+"embed")
            relation = next(x for x in rels if x.get("Id") == relationship_id)
            assert relation.get("TargetMode") != "External"
            part = posixpath.normpath(posixpath.join("ppt/slides",relation.get("Target")))
            assert part == f"ppt/media/project4-{key}.gif" and part in members
            blob = deck.read(part)
            with Image.open(BytesIO(blob)) as image:
                assert image.format == "GIF" and image.is_animated
                hashes, durations = [], []
                for i in range(image.n_frames):
                    image.seek(i)
                    hashes.append(sha256(image.convert("RGB").tobytes()).hexdigest())
                    durations.append(image.info.get("duration",0))
                assert len(set(hashes)) == image.n_frames and min(durations) > 0
                animations.append(dict(slide=n,asset=key,frames=image.n_frames,durations_ms=durations,
                                       distinct_frames=len(set(hashes)),sha256=sha256(blob).hexdigest()))
        assert notes == len(rows)
        assert len(animations) >= 12 and len(animations) == sum(x.endswith(".gif") for x in members)
    return dict(slides=len(rows),notes=notes,native_timing_slides=timing,
                transitions=transitions, videos=video,
                animated_media=len(animations),animations=animations)


def validate_browser(path, report):
    """Observe changing pixels in a local Chrome preview of the ZIP's GIF assets."""
    from tempfile import TemporaryDirectory
    from playwright.sync_api import sync_playwright

    with TemporaryDirectory() as directory, ZipFile(path) as deck, sync_playwright() as playwright:
        root = Path(directory)
        tags = []
        for row in report["animations"]:
            key = row["asset"]
            filename = f"project4-{key}.gif"
            (root/filename).write_bytes(deck.read(f"ppt/media/{filename}"))
            tags.append(f'<img width="240" height="100" alt="{key}" src="{filename}">')
        (root/"preview.html").write_text(
            '<meta charset="utf-8"><body style="margin:0;display:grid;grid-template-columns:repeat(6,240px)">' +
            "".join(tags) + "</body>", encoding="utf-8",
        )
        browser = playwright.chromium.launch(executable_path="/usr/bin/google-chrome")
        page = browser.new_page(viewport={"width":1440,"height":300})
        page.goto((root/"preview.html").as_uri())
        page.wait_for_function("Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)")
        initial = Image.open(BytesIO(page.screenshot())).convert("RGB")
        page.wait_for_timeout(2400)
        later = Image.open(BytesIO(page.screenshot())).convert("RGB")
        for i, row in enumerate(report["animations"]):
            x,y = (i%6)*240,(i//6)*100
            crop = (x,y,x+240,y+100)
            assert initial.crop(crop).tobytes() != later.crop(crop).tobytes(), row["asset"]
            row["browser_pixels_changed"] = True
        report["browser"] = browser.version
        report["browser_preview"] = "18 extraits du fichier PPTX et observés sous Chrome"
        browser.close()


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("poster",type=Path)
    cli.add_argument("--output",type=Path,default=Path("presentation/Data_Stream_Mining_Final_Anime.pptx"))
    cli.add_argument("--browser",action="store_true")
    args = cli.parse_args()
    rows = build(args.poster,args.output)
    report = validate(args.output,rows)
    if args.browser:
        validate_browser(args.output,report)
    Path("presentation/animation_validation.json").write_text(json.dumps(report,indent=2)+"\n")
    print(f"{report['slides']} diapositives, {report['notes']} notes, {report['animated_media']} GIF associés")
