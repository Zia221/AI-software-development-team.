from crewai.flow.flow import Flow, start, router, listen


class SoftwareFlow(Flow):

    @start()
    def start_project(self):

        print("🚀 Starting project...")

        return "Project started"

    @router(start_project)
    def check_project(self, message):

        print("🔀 Checking project...")

        bugs_found = True

        if bugs_found:
            return "bugs_found"

        return "no_bugs"

    @listen("bugs_found")
    def fix_bugs(self):

        print("🐛 Bugs found!")
        print("👨‍💻 Developer will fix them.")

        return "Bugs fixed"

    @listen("no_bugs")
    def finish_project(self):

        print("✅ No bugs found!")
        print("🎉 Project finished.")

        return "Project completed"


flow = SoftwareFlow()

result = flow.kickoff()

print("\nFinal result:")
print(result)