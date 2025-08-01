from pydantic import ValidationError


def log_validation_error(row_num: int, error: ValidationError) -> None:
    """Log the validation error to an error log file.

    Args:
        row_num (int): Row number in the CSV where the error occurred.
        error (ValidationError): Pydantic validation error.
    """
    with open("errors.log", "a") as f:
        f.write(f"Row {row_num}: {error}\n")
