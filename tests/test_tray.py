def test_tray_icon_creation():
    from tray import create_icon_image
    image = create_icon_image("green")
    assert image is not None
    assert image.size == (64, 64)
