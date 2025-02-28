from rich.progress import Progress
import time

with Progress() as progress:
    task1 = progress.add_task("[cyan]Processing...", total=100)
    task2 = progress.add_task("[blue]Processing...", total=100)
    task3 = progress.add_task("[red]Processing...", total=100)
    for i in range(100):
        time.sleep(0.05)  # Simulating work
        progress.update(task1, advance=1)
        progress.update(task2, advance=1)
        progress.update(task3, advance=1)
