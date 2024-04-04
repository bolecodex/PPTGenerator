def change_extension(filename, new_extension):
    # Split the filename into name and extension
    name, _ = filename.rsplit('.', 1)
    # Return the filename with the new extension
    return f"{name}.{new_extension}"