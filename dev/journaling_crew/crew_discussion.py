import datetime
import json
import uuid
import os

class JournalEntry:
    def __init__(self, thought, tags=None, context=None):
        self.timestamp = datetime.datetime.now().isoformat()
        self.entry_id = str(uuid.uuid4())
        self.thought = thought
        self.tags = tags if tags else []
        self.context = context if context else {}

    def to_dict(self):
        """Convert the journal entry to a dictionary for easy JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "entry_id": self.entry_id,
            "thought": self.thought,
            "tags": self.tags,
            "context": self.context
        }

class AgentJournal:
    def __init__(self, journal_path):
        self.journal_path = journal_path
        # Ensure the journal directory exists
        os.makedirs(os.path.dirname(journal_path), exist_ok=True)

    def write_entry(self, thought, tags=[], context={}):
        """Writes a new journal entry to the file."""
        entry = JournalEntry(thought, tags, context)
        with open(self.journal_path, "a") as file:
            json.dump(entry.to_dict(), file)
            file.write('\n')  # Ensure each entry is on a new line for easy reading

    def read_entries(self):
        """Reads all journal entries from the file."""
        entries = []
        try:
            with open(self.journal_path, 'r') as file:
                entries = [json.loads(line.strip()) for line in file]
        except FileNotFoundError:
            print("Journal file not found.")
        return entries

    def filter_entries_by_tag(self, filter_tags):
        """Filters entries by tags."""
        all_entries = self.read_entries()
        filtered_entries = [entry for entry in all_entries if any(tag in entry['tags'] for tag in filter_tags)]
        return filtered_entries

# Example usage of the AgentJournal
def main():
    # Initialize the journal for an agent
    agent_journal = AgentJournal("logs/agent_001_journal.txt")

    # Example of writing an entry
    agent_journal.write_entry(
        "Successfully integrated the new analysis algorithm, resulting in a 15% increase in efficiency.",
        tags=["success", "efficiency", "algorithm_integration"],
        context={"task_id": "task-12345", "outcome": "positive"}
    )

    # Reading and filtering entries
    entries = agent_journal.filter_entries_by_tag(["success"])
    for entry in entries:
        print(entry)

if __name__ == "__main__":
    main()
