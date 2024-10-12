import sys
import src.ratings.generate as g

args = sys.argv[1:]

rating_functions = {
    "faceoff": g.generate_faceoff,
    "defence": g.generate_defence,
}

if __name__ == '__main__':
    # Script here
    functions = []

    if len(args) == 0:
        user_input = None
        while user_input not in ["y", "n"]:
            print("You did not enter any arguments. Would you like to regenerate all of the ratings (y/n)?")
            user_input = input()
            if user_input == "y":
                functions.extend(rating_functions.values())
                break
            if user_input == "n":
                print("Exiting...")
                sys.exit(0)
    else:
        for arg in args:
            try:
                functions.append(rating_functions[arg])
            except KeyError:
                print(f"Could not find the rating function for {arg}, skipping...")
                continue

    for func in functions:
        print(f"Running {func.__name__}")
        func()

    print("All functions have been run! Exiting...")
