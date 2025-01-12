from dotenv import load_dotenv
import os

"""Updates or adds a key-value pair in the .env file."""
def update_env_file(key,value):
    env_file = ".env"
    load_dotenv(env_file)

    # Read current .env file contents
    with open(env_file,"r") as file:
        lines = file.readlines()
    
    # check if key exist 
    updated = False
    for i in range(len(lines)):
        if lines[i].startswith(f"{key}="):
            lines[i] =f"{key}={value}\n"
            updated = True
            break
    
    # If the key doesn't exist, add it
    if updated == False:
        lines.append(f"{key}={value}\n")

    # Write updated contents back to the .env file
    with open(env_file, "w") as file:
        file.writelines(lines)
    # print(f"Updated '{key}' in {env_file} to: {value}")

    #example usage
if __name__ == "__main__":
    # Example of adding or updating a token
    token = "example_new_token_valuedsdsdstestdsd"  # Replace with your actual token value
    update_env_file("ACCESS_TOKEN", token)
