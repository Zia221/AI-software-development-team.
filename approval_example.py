from crewai.flow.flow import Flow, start, router, listen


class ApprovalFlow(Flow):

    @start()
    def generate_code(self):

        print("🤖 AI Developer generated the code.")

        return "Code generated"

    @router(generate_code)
    def ask_for_approval(self, result):

        print("\n👤 Human Approval Required")

        approval = input("Approve the code? (yes/no): ")

        if approval.lower() == "yes":
            return "approved"

        return "rejected"

    @listen("approved")
    def send_to_qa(self):

        print("\n✅ Human approved the code.")
        print("🧪 Sending code to QA...")

        return "Sent to QA"

    @listen("rejected")
    def send_back_to_developer(self):

        print("\n❌ Human rejected the code.")
        print("👨‍💻 Sending code back to Developer...")

        return "Sent back to Developer"


flow = ApprovalFlow()

result = flow.kickoff()

print("\nFinal result:")
print(result)