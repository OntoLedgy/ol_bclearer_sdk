import subprocess

# Open the requirements.txt file and read dependencies
with open("requirements.txt") as file:
    for line in file:
        package = (
            line.strip()
        )  # Remove any extra whitespace
        if package:
            # Use poetry to add each package
            subprocess.run(
                [
                    "poetry",
                    "add",
                    package,
                ],
                check=False,
            )
