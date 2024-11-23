from dotenv import load_dotenv
from openai import OpenAI
import os

class ImageGenerator:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_cover(self, article_content: str) -> str:
        # 根据文章内容生成合适的提示词
        prompt = self._generate_prompt(article_content)

        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url

    def _generate_prompt(self, article_content: str) -> str:

        return f"Design an image for an article about: {article_content[:500]}. "


# 使用示例
if __name__ == "__main__":
    generator = ImageGenerator()
    article = "创业为导向的路线主要是指通过自己创业或者加入一个创业团队，实现自己更大的人生追求，比如财富自由，名利地位。它追求的是一个人生更大的可能性，在这种情况下没有一个确定的路径，理论上说只要你最后能成功，怎么做都可以。所以大厂并不是必须的选项，因为大厂确实能给你创业之路提供一些助力，但它同样也会带来一些缺点，并且绝对不会是你成功的核心因素，所以因人而异吧。"
    
    # ins_cover_url = generator.generate_cover(article, "instagram")
    # print(f"Instagram style cover URL: {ins_cover_url}")

    xhs_cover_url = generator.generate_cover(article, "xiaohongshu")
    print(f"Xiaohongshu style cover URL: {xhs_cover_url}")