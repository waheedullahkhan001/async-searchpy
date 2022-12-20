# Async search for a file in a directory tree

import pathlib
import asyncio
import time


tasks = []
results = []


async def search(path: str, keyword: str):
    try:
        path = pathlib.Path(path)
        if path.is_dir():
            # Iterate through the directory
            for file in path.iterdir():
                if file.is_dir():
                    # Create a new task for each directory and add it to the list of tasks
                    tasks.append(asyncio.create_task(search(file, keyword)))
                elif keyword in file.name:
                    print(file)
                    results.append(path)
        elif keyword in path.name:
            print(path)
            results.append(path)
    except PermissionError:
        pass

async def main(path: str, keyword: str):
    # Start the search
    await asyncio.create_task(search(path, keyword))
    
    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

    # Print the number of results
    print(f'Found {len(results)} results')

    # Print the results
    for result in results:
        print(result)


if __name__ == '__main__':
    input_path = input('Enter path to search: ')
    input_keyword = input('Enter keyword to search for: ')

    # Start the timer
    start_time = time.perf_counter()
    
    # Run the main function
    asyncio.run(main(input_path, input_keyword))

    # End the timer
    end_time = time.perf_counter()

    # Print the time it took to complete the search
    print(f'Finished in: {round((end_time - start_time) * 1000, 2)} ms')