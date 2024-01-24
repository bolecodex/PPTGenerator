def change_extension(filename, new_extension):
    # Split the filename into name and extension
    name, _ = filename.rsplit('.', 1)
    # Return the filename with the new extension
    return f"{name}.{new_extension}"

# Example usage
old_filename = "iwhefww.doc"
new_extension = "pptx"
new_filename = change_extension(old_filename, new_extension)

print(new_filename)