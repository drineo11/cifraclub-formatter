import pytest
from unittest.mock import patch, MagicMock
import io


class TestValidateUrl:
    def test_valid_url_https(self, client):
        response = client.post(
            "/api/generate",
            json={
                "url": "https://www.cifraclub.com.br/artista/musica/",
                "format": "docx",
            },
        )
        assert response.status_code in [200, 500]

    def test_valid_url_http(self, client):
        response = client.post(
            "/api/generate",
            json={
                "url": "http://www.cifraclub.com.br/artista/musica/",
                "format": "docx",
            },
        )
        assert response.status_code in [200, 500]

    def test_invalid_url_not_cifraclub(self, client):
        response = client.post(
            "/api/generate", json={"url": "https://www.google.com/", "format": "docx"}
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "cifraclub.com.br" in data["error"]

    def test_invalid_url_no_scheme(self, client):
        response = client.post(
            "/api/generate",
            json={"url": "www.cifraclub.com.br/artista/musica/", "format": "docx"},
        )
        assert response.status_code == 400

    def test_missing_url(self, client):
        response = client.post("/api/generate", json={"format": "docx"})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_invalid_format(self, client):
        with patch("api.index.get_cifra_content") as mock_get:
            mock_get.return_value = ("Title", "Artist", "Tom: C", [])
            response = client.post(
                "/api/generate",
                json={
                    "url": "https://www.cifraclub.com.br/artista/musica/",
                    "format": "txt",
                },
            )
            assert response.status_code == 400
            data = response.get_json()
            assert "error" in data


class TestGenerateEndpoint:
    def test_generate_docx_success(self, client):
        with patch("api.index.get_cifra_content") as mock_get:
            mock_get.return_value = ("Test Song", "Test Artist", "Tom: C", [])
            with patch("api.index.generate_docx_bytes") as mock_docx:
                mock_docx.return_value = b"fake docx content"
                response = client.post(
                    "/api/generate",
                    json={
                        "url": "https://www.cifraclub.com.br/artista/musica/",
                        "format": "docx",
                    },
                )
                assert response.status_code == 200
                assert "wordprocessingml" in response.content_type

    def test_generate_handles_exception(self, client):
        with patch("api.index.get_cifra_content") as mock_get:
            mock_get.side_effect = Exception("Site bloqueando")
            response = client.post(
                "/api/generate",
                json={
                    "url": "https://www.cifraclub.com.br/artista/musica/",
                    "format": "docx",
                },
            )
            assert response.status_code == 500
            data = response.get_json()
            assert "error" in data
