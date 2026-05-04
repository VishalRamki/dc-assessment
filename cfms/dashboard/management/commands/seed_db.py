from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from faker import Faker
import random

from dashboard.models import Area, Complaint, ComplaintCategory, ComplaintStatus, Notes, ServicePlan, UserProfile

fake = Faker()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        self.stdout.write("Seeding database...")
        # -------------------
        # STATUS
        # -------------------
        statuses = [
            "Open",
            "In Progress",
            "Escalated",
            "Resolved",
            "Closed",
        ]

        for name in statuses:
            ComplaintStatus.objects.get_or_create(name=name)

        # -------------------
        # CATEGORY
        # -------------------
        categories = [
            "Billing",
            "Network",
            "Device",
            "Roaming",
            "Other",
        ]

        for name in categories:
            ComplaintCategory.objects.get_or_create(name=name)

        areas = []
        for i in range(10):
            a,_ = Area.objects.get_or_create(name=fake.word())
            areas.append(a)

        ServicePlan.objects.get_or_create(name="Basic", data=5, call=100, sms=50)
        ServicePlan.objects.get_or_create(name="Standard", data=10, call=300, sms=150)
        ServicePlan.objects.get_or_create(name="Premium", data=50, call=1000, sms=500)

        # -------------------
        # GROUPS
        # -------------------
        customer_group, _ = Group.objects.get_or_create(name="Customer")
        agent_group, _ = Group.objects.get_or_create(name="Agent")
        admin_group, _ = Group.objects.get_or_create(name="Admin")

        # -------------------
        # USERS (SAFE - NO PKs)
        # -------------------
        def create_user(username, first, last, email, group):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "email": email,
                    "is_active": True
                }
            )
            user.set_password("Password.1")
            user.save()
            user.groups.add(group)

            # Create UserProfile safely (prevents duplicates)
            profile, _ = UserProfile.objects.get_or_create(user=user)

            # Assign random service plan if available
            plans = list(ServicePlan.objects.all())
            selected = random.choice(plans)
            if plans:
                profile.service_plan_ref = selected

            profile.sms = random.randint(1, selected.sms)
            profile.data = random.uniform(1.0, selected.data)
            profile.call = random.uniform(1.0, selected.call)
            profile.area_ref = random.choice(areas)

            profile.save()

            return user

        customers = [
            create_user("customer_emily", "Emily", "Watson", "emily@gmail.com", customer_group),
            create_user("customer_james", "James", "Walker", "james@gmail.com", customer_group),
            create_user("customer_sophia", "Sophia", "Brown", "sophia@gmail.com", customer_group),
            create_user("customer_daniel", "Daniel", "Cooper", "daniel@gmail.com", customer_group),
            create_user("customer_olivia", "Olivia", "Green", "olivia@gmail.com", customer_group),
        ]

        agents = [
            create_user("agent_maria", "Maria", "Lopez", "maria@support.com", agent_group),
            create_user("agent_noah", "Noah", "Taylor", "noah@support.com", agent_group),
            create_user("agent_ava", "Ava", "Thompson", "ava@support.com", agent_group),
        ]

        admin = create_user("admin_rachel", "Rachel", "Stewart", "rachel@company.com", admin_group)
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        # -------------------
        # LOOKUPS (NO HARDCODED IDS)
        # -------------------
        statuses = {s.name: s for s in ComplaintStatus.objects.all()}
        categories = list(ComplaintCategory.objects.all())

        status_flow = [
            "Open",
            "In Progress",
            "Escalated",
            "Resolved",
            "Closed"
        ]

        # -------------------
        # COMPLAINTS
        # -------------------
        Complaint.objects.all().delete()

        for i in range(30):

            customer = random.choice(customers)
            agent = random.choice(agents + [None])
            category = random.choice(categories)

            status_name = random.choice(status_flow)
            status = statuses.get(status_name)

            created = timezone.make_aware(
                fake.date_time_between(start_date="-60d", end_date="now")
            )

            last_update_date = timezone.make_aware(
                fake.date_time_between(start_date=created, end_date="now")
            )

            complaint = Complaint.objects.create(
                description=fake.sentence(nb_words=12),
                sub_date=created,
                last_update_date=created,
                customer_account_ref=customer,
                assigned_agent_ref=agent,
                complaint_category_ref=category,
                complaint_status_ref=status,
                area_ref=random.choice(areas)
            )

            num_notes = random.choices([0,1,2,3,4,5], weights=[10,20,25,20,15,10])[0]

            for i in range(num_notes):
                note = Notes.objects.create(
                    description=fake.sentence(nb_words=15),
                    last_update_date=timezone.make_aware(
                        fake.date_time_between(start_date=created, end_date=last_update_date)
                    ),
                    user_ref=random.choice([admin] + agents),
                )
                complaint.notes.add(note)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))