from uuid import uuid4


def generate_filename():
    return f"output_images/{uuid4()}.png"
