from db import init_db, list_unreviewed, approve_qa, delete_qa


def main():
    init_db()
    pending = list_unreviewed()
    if not pending:
        print("Nothing to review.")
        return

    for row in pending:
        print(f"\n[{row['id']}] Q: {row['question']}\n     A: {row['answer']}")
        choice = input("(a)pprove, (d)elete, (s)kip, (q)uit: ").strip().lower()
        if choice == "a":
            approve_qa(row["id"])
        elif choice == "d":
            delete_qa(row["id"])
        elif choice == "q":
            break


main()