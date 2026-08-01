from faker import Faker
from openpyxl import Workbook
from datetime import datetime

fake = Faker("en_IN")

TOTAL_USERS = 500
OUTPUT_FILE = "users_10k.xlsx"


def generate_excel():
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Users"

    # Excel headers
    headers = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "date_of_birth",
        "address",
        "city",
        "state",
        "pincode",
        "company",
        "job_title",
        "created_at",
    ]

    sheet.append(headers)

    print(f"Generating {TOTAL_USERS:,} users...")

    for index in range(1, TOTAL_USERS + 1):

        first_name = fake.first_name()
        last_name = fake.last_name()

        # Make email unique
        email = (
            f"{first_name.lower()}"
            f".{last_name.lower()}"
            f".{index}@example.com"
        )

        user = [
            first_name,
            last_name,
            email,
            fake.msisdn()[:10],
            fake.date_of_birth(
                minimum_age=18,
                maximum_age=65,
            ).strftime("%Y-%m-%d"),
            fake.address().replace("\n", ", "),
            fake.city(),
            fake.state(),
            fake.postcode(),
            fake.company(),
            fake.job(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ]

        sheet.append(user)

        # Progress
        if index % 1000 == 0:
            print(
                f"Generated {index:,}/{TOTAL_USERS:,} users"
            )

    workbook.save(OUTPUT_FILE)

    print("\nDone!")
    print(f"Generated: {TOTAL_USERS:,} users")
    print(f"File: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_excel()