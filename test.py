
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
import time 

console = Console()

# Exemple d'utilisation
with Progress(
    TextColumn("[bold blue]{task.percentage:>3.1f}%"),
    BarColumn(bar_width=None, complete_style="cyan", finished_style="red"),
    TextColumn("[bold blue]• {task.completed}/{task.total}"),
    console=console,
) as progress:
    task = progress.add_task("Chargement", total=576)

    for step in range(577):
        progress.update(task, advance=1)
        time.sleep(0.01)  # Simule un travail
