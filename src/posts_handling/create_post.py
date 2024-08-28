import os


async def create_post(dir: str, batch_size: int = 3):
    posts = []
    for filename in os.listdir(dir):
        if filename.lower().endswith(('.png', '.jpeg', '.jpg', '.gif', '.webp')):
            image_path = os.path.join(dir, filename)
            text_path = os.path.splitext(image_path)[0] + '.txt'
            if os.path.exists(text_path):
                with open(text_path, 'r', encoding='utf-8') as text_file:
                    text = text_file.read().strip()
            else:
                text = ''
            posts.append(
                {
                    'img': image_path,
                    'text': text,
                    'text_path': text_path
                })
            if len(posts) == batch_size:
                yield posts
                posts = []
    if posts:
        yield posts