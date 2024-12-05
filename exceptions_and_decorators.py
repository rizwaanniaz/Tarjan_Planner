import time
from datetime import datetime
from colorama import Fore, Style  # Used for colored console output (not currently used in this script)

# A logging decorator that can be temporarily disabled for debugging purposes
def logging_decorator(func):
    """
    A placeholder logging decorator. Currently disabled for simplicity.
    When required, this decorator can be enabled to log function execution
    details for debugging or troubleshooting.
    """
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)  # Simply calls the original function
    return wrapper

# Uncomment and modify the following code to enable logging functionality if needed
# def logging_decorator(func):
#     """
#     Logs the execution details of a function, including its name, arguments, and result.
#     Useful for troubleshooting and gaining insights into function behavior.
#     """
#     def wrapper(*args, **kwargs):
#         print(f"Executing: {func.__name__}")
#         print(f"Arguments: {args}, {kwargs}")
#         result = func(*args, **kwargs)
#         print(f"Result: {result}")
#         return result
#     return wrapper


# Decorator to measure and log the execution time of a function
def execution_time_decorator(func):
    """
    Measures the execution time of a function and logs the time to both the console
    and a log file. Optionally suppresses console output if needed.

    Logs include:
    - Function name
    - Execution time
    - Timestamp
    """
    def wrapper(*args, suppress_output=False, **kwargs):  # Allow suppress_output flag for optional console logging
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time

        # Get the current date and time for logging
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print execution details to the console unless suppressed
        if not suppress_output:
            print(f"{func.__name__} executed in {elapsed_time:.4f} seconds")

        # Log execution details to a file
        with open("journey_log.txt", "a") as log_file:
            log_file.write(
                f"Date and Time: {timestamp}\n"
                f"Function: {func.__name__}\n"
                f"Execution Time: {elapsed_time:.4f} seconds\n"
                "--------------------------------------------\n"
            )

        return result  # Return the result of the function
    return wrapper


# Decorator to handle and log errors during function execution
def error_handling_decorator(func):
    """
    Catches and logs exceptions raised during the execution of a function.
    Prints an error message to the console and re-raises the exception.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Attempt to execute the function
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")  # Print error details
            raise  # Re-raise the exception for further handling
    return wrapper
