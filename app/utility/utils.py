import re


def camel_to_snake(camel_str):
    """
    As per pylint, Snake case will be used for most of the python variables and thus, mostly client facing variables
    """
    # Add an underscore before any uppercase letter (except the first one) and convert the string to lowercase
    snake_str = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    snake_str = re.sub("([a-z0-9])([A-Z])", r"\1_\2", snake_str).lower()
    return snake_str


def snake_to_camel(snake_str):
    """
    Camel case will be used for DB attributes
    """
    # Split the string by underscores and capitalize each part, then join them
    components = snake_str.split("_")
    camel_str = components[0] + "".join(x.title() for x in components[1:])
    return camel_str


def is_valid_website(website):
    """
    Validate if the website is in a cleaned format.
    """
    # Check if the website starts with http:// or https://
    if website.startswith(("http://", "https://", "www")):
        return False

    # Simple regex for validating a website (you can customize this as needed)
    website_regex = re.compile(
        r"^(https?:\/\/)?"  # http:// or https://
        r"([a-zA-Z0-9-]+\.)+"  # Domain name
        r"[a-zA-Z]{2,6}"  # Domain extension
        r"([\/\w .-]*)*\/?$"  # Path
    )

    return re.match(website_regex, website) is not None
