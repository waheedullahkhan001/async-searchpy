# Async search for a file in a directory tree

import pathlib
import asyncio
import time

# List to store tasks
tasks = []

# List to store results
results = []

# Function to search for a given keyword in the file names within a directory
async def search(path: pathlib.Path, keyword: str, dirs: list[pathlib.Path]):
    # Try to iterate through the contents of the directory
    try:
        # Iterate through the contents of the directory
        for child in path.iterdir():
            # If the keyword is in the file name, append it to the results list
            if keyword in child.name.lower():
                print(child)
                results.append(child)

            # If the item is a directory, add it to the dirs list
            if child.is_dir():
                dirs.append(child)
    # Catch any OSErrors
    except OSError:
        pass

# Function to search all directories in the list
async def search_all(paths: list[pathlib.Path], keyword: str) -> list[pathlib.Path]:
    # List to store subdirectories
    dirs = []

    # Create a task for each path
    for path in paths:
        search_task = asyncio.create_task(search(path, keyword, dirs))
        tasks.append(search_task)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

    # Clear the tasks list
    tasks.clear()
    
    return dirs

async def main(path: pathlib.Path, keyword: str):
    # Start the search
    dirs_remaining = await asyncio.create_task(search_all([path], keyword))
    while dirs_remaining:
        dirs_remaining = await asyncio.create_task(search_all(dirs_remaining, keyword))

    # Print the number of results
    print(f'Found {len(results)} results')

    # Print the results
    for result in results:
        print(result)


if __name__ == '__main__':
    # Get the path and keyword to search for
    input_path = input('Enter path to search: ')
    input_path = pathlib.Path(input_path)
    # Validate that the input path exists and is a directory
    while not input_path.exists() or not input_path.is_dir():
        input_path = input('Invalid path. Enter path to search: ')
        input_path = pathlib.Path(input_path)
    
    input_keyword = input('Enter keyword to search for: ').lower()
    # Validate that the input keyword is not empty
    while not input_keyword:
        input_keyword = input('Invalid keyword. Enter keyword to search for: ').lower()

    # Start the timer
    start_time = time.perf_counter()
    
    # Run the main function
    asyncio.run(main(input_path, input_keyword))

    # End the timer
    end_time = time.perf_counter()

    # Print the time taken
    print(f'Time taken: {end_time - start_time} seconds')
