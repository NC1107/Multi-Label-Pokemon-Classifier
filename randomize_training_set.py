import os
import random
from distutils.dir_util import copy_tree
import shutil

# the goal of this class is to randomize the images by moving them to either training or testing folders

training_ratio = 0.8
image_directory = "data/images/"
testing_directory = "data/testing_set/"
training_directory = "data/training_set/"


def populate_sets():
    # check if directories exist
    if not os.path.exists(training_directory) or not os.path.exists(testing_directory):
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
        training_set = images[:int(len(images) * training_ratio)]
        testing_set = images[int(len(images) * training_ratio):]
        copy_tree(image_directory + pokemon, training_directory + pokemon, verbose=0)
        copy_tree(image_directory + pokemon, testing_directory + pokemon, verbose=0)
        for image in training_set:
            os.remove(training_directory + pokemon + "/" + image)
        for image in testing_set:
            os.remove(testing_directory + pokemon + "/" + image)


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


def cleanup_directories():
    if os.path.exists(training_directory):
        print("removing training directory")
        shutil.rmtree(training_directory)

    if os.path.exists(testing_directory):
        print("removing testing directory")
        shutil.rmtree(testing_directory)


def main():
    choice = "0"
    while choice != "4":
        print("1: generate directories")
        print("2: cleanup directories")
        print("3: populate sets")
        print("4: exit")
        choice = input("enter choice: ")
        match choice:
            case "1":
                generate_directories()
            case "2":
                cleanup_directories()
            case "3":
                populate_sets()
            case "4":
                print("exiting")
            case _:
                print("invalid")


if __name__ == "__main__":
    main()
