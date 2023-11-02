# convert all images to
import os
from PIL import Image


def convert_images():
    # for all images in data/images, convert to png and remove original
    for pokemon in os.listdir("data/images"):
        for image in os.listdir("data/images/" + pokemon):
            if image.endswith(".jpg"):
                im = Image.open("data/images/" + pokemon + "/" + image)
                im.save("data/images/" + pokemon + "/" + image.replace(".jpg", ".png"))
                os.remove("data/images/" + pokemon + "/" + image)
                print("converted " + image)
            if image.endswith(".jpeg"):
                im = Image.open("data/images/" + pokemon + "/" + image)
                im.save("data/images/" + pokemon + "/" + image.replace(".jpeg", ".png"))
                os.remove("data/images/" + pokemon + "/" + image)
                print("converted " + image)
            if image.endswith(".svg"):
                # delete svg, annoying to handle for some reason
                os.remove("data/images/" + pokemon + "/" + image)


def main():
    convert_images()


if __name__ == "__main__":
    main()
