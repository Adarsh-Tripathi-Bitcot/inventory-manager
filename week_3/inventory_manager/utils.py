from pydantic import ValidationError

def log_validation_error(row_num: int, error: ValidationError) -> None:
    """
    Logs the validation error for a row in the errors.log file.

    Args:
        row_num (int): The row number where the error occurred.
        error (ValidationError): The validation error object.
    """
    with open("errors.log", "a") as f:
        f.write(f"Row {row_num}: {error}\n")
