import unittest

from src.app.web_app import create_app


class WebAppSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_page_renders(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("图斑审查预检系统".encode("utf-8"), response.data)

    def test_form_submission_returns_result(self) -> None:
        response = self.client.post(
            "/",
            data={
                "parcel_id": "FJ-WEB-001",
                "image_path": "demo.jpg",
                "land_type": "耕地",
                "text_description": "地块申报为耕地，但描述中出现疑似建筑物，且拍摄角度有限。",
                "rules": "若耕地中出现疑似建筑物，应标记为疑似异常。\n若证据不足，应建议人工复核。",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("耕地疑似建筑占用".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
