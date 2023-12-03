import os
import random
from PIL import Image
import shutil
from distutils.dir_util import copy_tree
import keras
import tensorflow as tf

training_ratio = 0.8
image_directory = "data/images/"
rotated_directory = "data/rotated_set/"
testing_directory = "data/testing_set/"
training_directory = "data/training_set/"


def populate_sets():
    # check if directories exist
    if not os.path.exists(training_directory) or not os.path.exists(testing_directory) or not os.path.exists(
            rotated_directory):
        print("Directories not found")
        return
    # check if directories are empty
    if os.listdir(training_directory) != [] or os.listdir(testing_directory) != []:
        print("Directories not empty")
        return
    # iterate through all pokemon, place 80% of each pokemons images in training set, 20% in testing set
    for pokemon in os.listdir(image_directory):
        images = os.listdir(image_directory + pokemon)
        random.shuffle(images)
        training_set = images[int(len(images) * training_ratio):]
        testing_set = images[:int(len(images) * training_ratio)]
        copy_tree(image_directory + pokemon, training_directory + pokemon, verbose=0)
        copy_tree(image_directory + pokemon, testing_directory + pokemon, verbose=0)
        for image in training_set:
            os.remove(training_directory + pokemon + "/" + image)
        for image in testing_set:
            os.remove(testing_directory + pokemon + "/" + image)

    # iterate through all pokemon, place 80% of each pokemons images in training set, 20% in testing set
    for pokemon in os.listdir(rotated_directory):
        copy_tree(rotated_directory + pokemon, training_directory + pokemon, verbose=0)


def generate_directories():
    if not os.path.exists(image_directory):
        print("image dataset not found")
        exit(0)
    if not os.path.exists(training_directory):
        print("generating training directory")
        os.makedirs(training_directory)
    if not os.path.exists(testing_directory):
        print("generating testing directory")
        os.makedirs(testing_directory)
    if not os.path.exists(rotated_directory):
        print("generating rotated directory")
        os.makedirs(rotated_directory)


def cleanup_directories():
    if os.path.exists(training_directory):
        print("removing training directory")
        shutil.rmtree(training_directory)

    if os.path.exists(testing_directory):
        print("removing testing directory")
        shutil.rmtree(testing_directory)


def generate_rotated_images():
    for pokemon in os.listdir(image_directory):
        for image in os.listdir(image_directory + pokemon):
            original = Image.open(image_directory + pokemon + "/" + image)

            rotate90 = original.rotate(90)
            rotate180 = original.rotate(180)
            rotate270 = original.rotate(270)
            mirrored = original.transpose(method=Image.FLIP_LEFT_RIGHT)

            rotate90.save(rotated_directory + pokemon + "/" + "rotate90" + image)
            rotate180.save(rotated_directory + pokemon + "/" + "rotate180" + image)
            rotate270.save(rotated_directory + pokemon + "/" + "rotate270" + image)
            mirrored.save(rotated_directory + pokemon + "/" + "mirrored" + image)


def automatically_setup_repository():
    cleanup_directories()
    print("----CLEANUP COMPLETE----")
    generate_directories()
    print("----DIRECTORIES GENERATED----")
    if not os.path.exists(rotated_directory):
        generate_rotated_images()
    print("----ROTATED IMAGES GENERATED----")
    populate_sets()
    print("----SETS POPULATED----")


def setup_repository():
    choice = "0"
    while choice != "5":
        print("1: generate directories")
        print("2: cleanup directories")
        print("3: populate sets")
        print("4: generate rotated images")
        print("5: exit")
        choice = input("enter choice: ")
        match choice:
            case "1":
                generate_directories()
            case "2":
                cleanup_directories()
            case "3":
                populate_sets()
            case "4":
                generate_rotated_images()
            case "5":
                print("exiting")
            case _:
                print("invalid")


def convert_dataset_images_to_png():
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


def pick_random_image() -> str:
    # get the list of Pokémon
    pokemon = os.listdir("data/images")
    # pick a random pokemon
    random_pokemon = pokemon[random.randint(0, len(pokemon) - 1)]
    # get the list of images for that Pokémon
    images = os.listdir("data/images/" + random_pokemon)
    # pick a random image
    random_image = images[random.randint(0, len(images) - 1)]
    # return the full path to the image
    return "data/images/" + random_pokemon + "/" + random_image


def pick_random_rotated_image() -> str:
    # get the list of Pokémon
    pokemon = os.listdir("data/rotated_set")
    # pick a random pokemon
    random_pokemon = pokemon[random.randint(0, len(pokemon) - 1)]
    # get the list of images for that Pokémon
    images = os.listdir("data/rotated_set/" + random_pokemon)
    # pick a random image
    random_image = images[random.randint(0, len(images) - 1)]
    # return the full path to the image
    return "data/rotated_set/" + random_pokemon + "/" + random_image


# function to load and test the model on a random image
