from streamlit.testing.v1 import AppTest


def click(app, label):
    next(button for button in app.button if button.label == label).click().run()
    assert not app.exception


def test_dashboard_controls():
    app = AppTest.from_file("dashboard/app.py").run()
    assert not app.exception
    click(app, "Avancer d’un événement")
    assert app.metric[0].value == "200"
    click(app, "Simuler un incident")
    click(app, "Avancer d’un lot")
    assert app.metric[-1].value == "Alerte"
    click(app, "Revenir à la normale")
    for _ in range(5):
        click(app, "Avancer d’un lot")
    assert app.metric[-1].value == "Normal"
    click(app, "Démarrer")
    click(app, "Pause")
    click(app, "Réinitialiser")
    assert not app.metric
