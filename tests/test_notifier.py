def test_pushme_client_init():
    from notifier import PushMeClient
    client = PushMeClient("test_key")
    assert client.push_key == "test_key"
