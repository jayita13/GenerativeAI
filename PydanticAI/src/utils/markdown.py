from pydantic import BaseModel


def to_markdown(data, indent=0):
    markdown = ""
    if isinstance(data, BaseModel):
        data = data.model_dump()
    if isinstance(data, dict):
        for key, value in data.items():
            markdown += f"{'#' * (indent + 2)} {key.upper()}\n"
            if isinstance(value, (dict, list, BaseModel)):
                markdown += to_markdown(value, indent + 1)
            else:
                markdown += f"{value}\n\n"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list, BaseModel)):
                markdown += to_markdown(item, indent)
            else:
                markdown += f"- {item}\n"
        markdown += "\n"
    else:
        markdown += f"{data}\n\n"
    return markdown
