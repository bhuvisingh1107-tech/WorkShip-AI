"""Idempotent enterprise seed data for WorkShip Technologies."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, initialize_database
from app.models import Document, Employee, Incident, LogEntry, Meeting, Service, Team


@dataclass
class SectionSummary:
    inserted: int = 0
    skipped: int = 0


TEAM_DATA = [
    ("Engineering", "Builds and operates WorkShip's product and platform."),
    ("IT Operations", "Maintains enterprise systems, endpoint management, and access."),
    ("Security", "Protects company systems, data, and incident response operations."),
    ("Human Resources", "Supports talent, culture, people operations, and employee programs."),
    ("Finance", "Leads financial planning, payroll, expense management, and reporting."),
]

EMPLOYEE_DATA = [
    ("Avery Chen", "avery.chen@workship.tech", "Chief Executive Officer", "Engineering", None),
    ("Maya Patel", "maya.patel@workship.tech", "Chief Technology Officer", "Engineering", "avery.chen@workship.tech"),
    ("Daniel Brooks", "daniel.brooks@workship.tech", "Engineering Manager, Backend", "Engineering", "maya.patel@workship.tech"),
    ("Sofia Ramirez", "sofia.ramirez@workship.tech", "Engineering Manager, Frontend", "Engineering", "maya.patel@workship.tech"),
    ("Ethan Walker", "ethan.walker@workship.tech", "Platform Engineering Manager", "Engineering", "maya.patel@workship.tech"),
    ("Priya Nair", "priya.nair@workship.tech", "Security Lead", "Security", "avery.chen@workship.tech"),
    ("Olivia Grant", "olivia.grant@workship.tech", "Human Resources Director", "Human Resources", "avery.chen@workship.tech"),
    ("Marcus Reed", "marcus.reed@workship.tech", "Finance Manager", "Finance", "avery.chen@workship.tech"),
    ("Noah Davis", "noah.davis@workship.tech", "IT Operations Manager", "IT Operations", "avery.chen@workship.tech"),
    ("Liam Foster", "liam.foster@workship.tech", "Senior Backend Engineer", "Engineering", "daniel.brooks@workship.tech"),
    ("Grace Kim", "grace.kim@workship.tech", "Backend Engineer", "Engineering", "daniel.brooks@workship.tech"),
    ("Henry Ortiz", "henry.ortiz@workship.tech", "Backend Engineer", "Engineering", "daniel.brooks@workship.tech"),
    ("Chloe Martin", "chloe.martin@workship.tech", "Backend Engineer", "Engineering", "daniel.brooks@workship.tech"),
    ("Isaac Turner", "isaac.turner@workship.tech", "Backend Engineer", "Engineering", "daniel.brooks@workship.tech"),
    ("Zoe Bennett", "zoe.bennett@workship.tech", "Backend Engineer", "Engineering", "daniel.brooks@workship.tech"),
    ("Caleb Morris", "caleb.morris@workship.tech", "Backend Engineer", "Engineering", "daniel.brooks@workship.tech"),
    ("Emma Wilson", "emma.wilson@workship.tech", "Senior Frontend Engineer", "Engineering", "sofia.ramirez@workship.tech"),
    ("Lucas Price", "lucas.price@workship.tech", "Frontend Engineer", "Engineering", "sofia.ramirez@workship.tech"),
    ("Harper Lee", "harper.lee@workship.tech", "Frontend Engineer", "Engineering", "sofia.ramirez@workship.tech"),
    ("Owen Scott", "owen.scott@workship.tech", "Frontend Engineer", "Engineering", "sofia.ramirez@workship.tech"),
    ("Mia Cooper", "mia.cooper@workship.tech", "Frontend Engineer", "Engineering", "sofia.ramirez@workship.tech"),
    ("Jack Rivera", "jack.rivera@workship.tech", "Frontend Engineer", "Engineering", "sofia.ramirez@workship.tech"),
    ("Aria Thompson", "aria.thompson@workship.tech", "Senior DevOps Engineer", "Engineering", "ethan.walker@workship.tech"),
    ("Leo Parker", "leo.parker@workship.tech", "DevOps Engineer", "Engineering", "ethan.walker@workship.tech"),
    ("Nora Hughes", "nora.hughes@workship.tech", "Platform Engineer", "Engineering", "ethan.walker@workship.tech"),
    ("Finn Coleman", "finn.coleman@workship.tech", "Platform Engineer", "Engineering", "ethan.walker@workship.tech"),
    ("Ava Collins", "ava.collins@workship.tech", "Site Reliability Engineer", "Engineering", "ethan.walker@workship.tech"),
    ("Samuel King", "samuel.king@workship.tech", "IT Administrator", "IT Operations", "noah.davis@workship.tech"),
    ("Ella Ward", "ella.ward@workship.tech", "IT Administrator", "IT Operations", "noah.davis@workship.tech"),
    ("Julian Ross", "julian.ross@workship.tech", "IT Support Specialist", "IT Operations", "noah.davis@workship.tech"),
    ("Amelia Bell", "amelia.bell@workship.tech", "Endpoint Management Engineer", "IT Operations", "noah.davis@workship.tech"),
    ("Ravi Shah", "ravi.shah@workship.tech", "Security Engineer", "Security", "priya.nair@workship.tech"),
    ("Isabella Young", "isabella.young@workship.tech", "Security Analyst", "Security", "priya.nair@workship.tech"),
    ("Theo Adams", "theo.adams@workship.tech", "Cloud Security Engineer", "Security", "priya.nair@workship.tech"),
    ("Claire Evans", "claire.evans@workship.tech", "People Operations Manager", "Human Resources", "olivia.grant@workship.tech"),
    ("Ben Harris", "ben.harris@workship.tech", "Talent Acquisition Partner", "Human Resources", "olivia.grant@workship.tech"),
    ("Ruby Flores", "ruby.flores@workship.tech", "HR Business Partner", "Human Resources", "olivia.grant@workship.tech"),
    ("George Long", "george.long@workship.tech", "Senior Financial Analyst", "Finance", "marcus.reed@workship.tech"),
    ("Hannah Cox", "hannah.cox@workship.tech", "Payroll Specialist", "Finance", "marcus.reed@workship.tech"),
    ("Victor Perry", "victor.perry@workship.tech", "Accounts Payable Specialist", "Finance", "marcus.reed@workship.tech"),
]

SERVICE_DATA = [
    ("WorkShip Web Portal", "Employee-facing workplace assistant web application.", "Engineering", "high"),
    ("Identity Gateway", "Single sign-on and internal identity federation service.", "Security", "critical"),
    ("Employee Directory", "Authoritative employee profile and organizational directory.", "Human Resources", "high"),
    ("Incident Command Center", "Incident coordination and communications platform.", "Engineering", "critical"),
    ("Knowledge Hub", "Enterprise documentation and policy knowledge base.", "Engineering", "high"),
    ("Observability Platform", "Centralized metrics, traces, alerts, and logs platform.", "Engineering", "critical"),
    ("CI/CD Platform", "Continuous integration and deployment pipeline service.", "Engineering", "high"),
    ("Data Warehouse", "Company reporting and analytics data warehouse.", "Finance", "high"),
    ("Payroll Processing", "Payroll calculation and payment operations service.", "Finance", "critical"),
    ("Expense Management", "Employee expense submission and approval service.", "Finance", "medium"),
    ("Endpoint Management", "Corporate device inventory and endpoint configuration service.", "IT Operations", "high"),
    ("Security Operations Center", "Security event monitoring and response service.", "Security", "critical"),
    ("VPN Gateway", "Secure remote access service for employees and contractors.", "IT Operations", "critical"),
    ("Collaboration Suite", "Internal messaging, calendar, and collaboration integrations.", "IT Operations", "medium"),
    ("Notification Service", "Cross-platform employee and operational notification delivery.", "Engineering", "high"),
]

DOCUMENT_TOPICS = {
    "Engineering": [
        "Platform Architecture Overview", "API Development Standards", "Frontend Engineering Guide", "Backend Engineering Guide", "Production Release Checklist", "On-Call Handbook", "Code Review Standards", "Service Ownership Policy", "Observability Playbook", "Disaster Recovery Runbook"
    ],
    "IT Operations": [
        "Endpoint Enrollment Guide", "Corporate Device Policy", "VPN Access Guide", "IT Service Request Process", "Incident Escalation Matrix", "Identity Access Provisioning", "Collaboration Suite Guide", "Network Change Procedure", "Asset Management Standard", "Business Continuity Contacts"
    ],
    "Security": [
        "Information Security Policy", "Secure Development Standard", "Phishing Response Guide", "Security Incident Response Plan", "Access Review Procedure", "Data Classification Standard", "Vendor Risk Assessment Guide", "Vulnerability Management Policy", "Security Awareness Handbook", "Privileged Access Procedure"
    ],
    "Human Resources": [
        "Employee Handbook", "New Hire Onboarding Guide", "Performance Review Process", "Remote Work Policy", "Leave and Benefits Guide", "Career Development Framework", "Manager Coaching Guide", "Workplace Conduct Policy", "Compensation Philosophy", "Employee Recognition Program"
    ],
    "Finance": [
        "Annual Budget Planning Guide", "Expense Reimbursement Policy", "Procurement Approval Matrix", "Month-End Close Checklist", "Revenue Recognition Overview", "Travel and Entertainment Policy", "Financial Controls Handbook", "Vendor Payment Procedure", "Forecasting Methodology", "Audit Readiness Guide"
    ],
}

INCIDENT_DATA = [
    ("Identity Gateway elevated authentication failures", "critical", "resolved", "Identity Gateway", "Security", "Authentication requests exceeded the error threshold.", "An expired signing certificate was rotated and trust stores were refreshed."),
    ("Web Portal API latency increase", "high", "resolved", "WorkShip Web Portal", "Engineering", "Employee portal response times exceeded the service objective.", "A database query regression was optimized and released."),
    ("VPN Gateway connection instability", "high", "resolved", "VPN Gateway", "IT Operations", "Remote employees experienced intermittent VPN reconnections.", "A faulty gateway node was removed from the load balancer."),
    ("Payroll Processing delayed batch", "critical", "resolved", "Payroll Processing", "Finance", "Scheduled payroll processing completed later than planned.", "A dependency timeout was increased after vendor maintenance."),
    ("Knowledge Hub search index delay", "medium", "resolved", "Knowledge Hub", "Engineering", "New documents were delayed before becoming searchable.", "Background workers were scaled and a queue backlog was drained."),
    ("Endpoint Management enrollment backlog", "medium", "resolved", "Endpoint Management", "IT Operations", "New corporate devices remained pending enrollment.", "An enrollment token configuration was corrected."),
    ("Observability Platform alert delivery gap", "high", "resolved", "Observability Platform", "Engineering", "Several on-call notifications were delayed.", "A notification provider rate limit was adjusted."),
    ("Security Operations Center ingestion lag", "high", "resolved", "Security Operations Center", "Security", "Security event ingestion was delayed during peak volume.", "Parsing workers were autoscaled and malformed events were quarantined."),
    ("Expense Management attachment upload issue", "low", "resolved", "Expense Management", "Finance", "Some expense attachments could not be uploaded.", "A storage policy mismatch was corrected."),
    ("CI/CD Platform build queue saturation", "medium", "resolved", "CI/CD Platform", "Engineering", "Build wait times increased for engineering teams.", "Additional runners were provisioned for peak hours."),
    ("Employee Directory profile sync delay", "medium", "resolved", "Employee Directory", "Human Resources", "Recently updated employee profiles were not immediately visible.", "A failed synchronization job was retried."),
    ("Data Warehouse nightly load failure", "high", "resolved", "Data Warehouse", "Finance", "Nightly analytics data was incomplete.", "A source schema change was accommodated in the load job."),
    ("Collaboration Suite calendar integration issue", "low", "resolved", "Collaboration Suite", "IT Operations", "Some calendar updates were not synchronized.", "An OAuth consent scope was renewed."),
    ("Notification Service duplicate messages", "medium", "resolved", "Notification Service", "Engineering", "A subset of notifications was delivered twice.", "Message deduplication keys were restored."),
    ("Incident Command Center timeline rendering issue", "low", "resolved", "Incident Command Center", "Engineering", "Incident timeline entries briefly rendered out of order.", "Client-side ordering logic was corrected."),
    ("Identity Gateway maintenance alert", "low", "closed", "Identity Gateway", "Security", "Planned certificate renewal maintenance notification.", "Planned maintenance completed without customer impact."),
    ("Web Portal accessibility regression", "medium", "resolved", "WorkShip Web Portal", "Engineering", "Keyboard navigation was impaired on one portal view.", "The affected component was updated and verified."),
    ("VPN Gateway capacity warning", "medium", "monitoring", "VPN Gateway", "IT Operations", "Concurrent connection volume approached the configured capacity threshold.", "Capacity expansion is scheduled before the next planning cycle."),
    ("Observability Platform storage warning", "low", "monitoring", "Observability Platform", "Engineering", "Log retention storage approached the warning threshold.", "Retention policies are being reviewed with service owners."),
    ("Security Operations Center rule tuning", "low", "closed", "Security Operations Center", "Security", "A detection rule generated an elevated number of benign alerts.", "The rule threshold was tuned after analyst review."),
]

MEETING_DATA = [
    ("Executive Operating Review", date(2026, 1, 5), ["avery.chen@workship.tech", "maya.patel@workship.tech", "marcus.reed@workship.tech"], "Leadership reviewed operating metrics, enterprise risks, and quarterly priorities."),
    ("Engineering Architecture Council", date(2026, 1, 7), ["maya.patel@workship.tech", "daniel.brooks@workship.tech", "sofia.ramirez@workship.tech", "ethan.walker@workship.tech"], "Engineering leaders aligned on platform reliability and API modernization work."),
    ("Security Risk Review", date(2026, 1, 9), ["priya.nair@workship.tech", "ravi.shah@workship.tech", "theo.adams@workship.tech"], "Security reviewed open risks, detection coverage, and access review milestones."),
    ("People Operations Planning", date(2026, 1, 12), ["olivia.grant@workship.tech", "claire.evans@workship.tech", "ruby.flores@workship.tech"], "HR reviewed onboarding capacity, performance review preparation, and benefits communications."),
    ("Finance Forecast Review", date(2026, 1, 14), ["marcus.reed@workship.tech", "george.long@workship.tech", "hannah.cox@workship.tech"], "Finance reviewed the annual operating forecast and month-end readiness."),
    ("Production Readiness Review", date(2026, 1, 16), ["ethan.walker@workship.tech", "aria.thompson@workship.tech", "leo.parker@workship.tech"], "Platform engineering reviewed deployment safeguards and capacity planning."),
    ("IT Operations Service Review", date(2026, 1, 19), ["noah.davis@workship.tech", "samuel.king@workship.tech", "ella.ward@workship.tech"], "IT Operations reviewed endpoint health, VPN capacity, and service desk metrics."),
    ("Incident Retrospective: Identity Gateway", date(2026, 1, 21), ["priya.nair@workship.tech", "maya.patel@workship.tech", "ravi.shah@workship.tech"], "The team reviewed the authentication failure incident and follow-up actions."),
    ("Engineering All-Hands", date(2026, 1, 23), ["maya.patel@workship.tech", "daniel.brooks@workship.tech", "sofia.ramirez@workship.tech", "ethan.walker@workship.tech"], "Engineering shared delivery progress, reliability updates, and team announcements."),
    ("Quarterly Business Planning", date(2026, 1, 26), ["avery.chen@workship.tech", "olivia.grant@workship.tech", "marcus.reed@workship.tech", "maya.patel@workship.tech"], "Leadership finalized enterprise objectives, staffing plans, and investment priorities."),
]

LOG_START = datetime(2026, 1, 27, 8, 0, tzinfo=timezone.utc)
LOG_LEVELS = ["INFO", "INFO", "INFO", "WARNING", "ERROR"]
LOG_MESSAGES = [
    "Health check completed successfully", "Scheduled workflow completed", "Configuration refresh applied", "Request latency remains within target", "Background worker processed queued items", "Access policy evaluation completed", "Service dependency check passed", "Capacity utilization recorded", "Audit event persisted", "Retryable operation completed"
]


def seed_teams(session: Session) -> tuple[SectionSummary, dict[str, Team]]:
    summary = SectionSummary()
    teams: dict[str, Team] = {}
    for name, description in TEAM_DATA:
        team = session.scalar(select(Team).where(Team.name == name))
        if team is None:
            team = Team(name=name, description=description)
            session.add(team)
            summary.inserted += 1
        else:
            summary.skipped += 1
        teams[name] = team
    session.commit()
    return summary, teams


def seed_employees(session: Session, teams: dict[str, Team]) -> SectionSummary:
    summary = SectionSummary()
    employees: dict[str, Employee] = {
        employee.email: employee for employee in session.scalars(select(Employee)).all()
    }
    for full_name, email, role, team_name, manager_email in EMPLOYEE_DATA:
        if email in employees:
            summary.skipped += 1
            continue
        manager = employees.get(manager_email) if manager_email else None
        employee = Employee(
            full_name=full_name,
            email=email,
            role=role,
            team_id=teams[team_name].id,
            manager=manager,
        )
        session.add(employee)
        employees[email] = employee
        summary.inserted += 1
    session.commit()
    return summary


def seed_services(session: Session, teams: dict[str, Team]) -> tuple[SectionSummary, dict[str, Service]]:
    summary = SectionSummary()
    services: dict[str, Service] = {}
    for name, description, owner_team, criticality in SERVICE_DATA:
        service = session.scalar(select(Service).where(Service.name == name))
        if service is None:
            service = Service(
                name=name,
                description=description,
                owner_team_id=teams[owner_team].id,
                criticality=criticality,
            )
            session.add(service)
            summary.inserted += 1
        else:
            summary.skipped += 1
        services[name] = service
    session.commit()
    return summary, services


def seed_documents(session: Session) -> SectionSummary:
    summary = SectionSummary()
    for team, topics in DOCUMENT_TOPICS.items():
        for topic in topics:
            title = f"{team}: {topic}"
            document = session.scalar(select(Document).where(Document.title == title))
            if document is not None:
                summary.skipped += 1
                continue
            session.add(
                Document(
                    title=title,
                    category=team,
                    source="WorkShip Internal Knowledge Base",
                    content=(
                        f"This WorkShip Technologies {team} document defines the "
                        f"enterprise standard for {topic.lower()}. It is maintained "
                        "by the responsible team and reviewed during the annual policy cycle."
                    ),
                )
            )
            summary.inserted += 1
    session.commit()
    return summary


def seed_incidents(
    session: Session, teams: dict[str, Team], services: dict[str, Service]
) -> SectionSummary:
    summary = SectionSummary()
    for title, severity, incident_status, service_name, owner_team, summary_text, root_cause in INCIDENT_DATA:
        incident = session.scalar(select(Incident).where(Incident.title == title))
        if incident is not None:
            summary.skipped += 1
            continue
        session.add(
            Incident(
                title=title,
                severity=severity,
                status=incident_status,
                service_id=services[service_name].id,
                owner_team_id=teams[owner_team].id,
                summary=summary_text,
                root_cause=root_cause,
            )
        )
        summary.inserted += 1
    session.commit()
    return summary


def seed_meetings(session: Session) -> SectionSummary:
    summary = SectionSummary()
    for title, meeting_date, participants, transcript in MEETING_DATA:
        meeting = session.scalar(select(Meeting).where(Meeting.title == title))
        if meeting is not None:
            summary.skipped += 1
            continue
        session.add(
            Meeting(
                title=title,
                date=meeting_date,
                participants=participants,
                transcript=transcript,
            )
        )
        summary.inserted += 1
    session.commit()
    return summary


def seed_log_entries(session: Session) -> SectionSummary:
    summary = SectionSummary()
    service_names = [service[0] for service in SERVICE_DATA]
    for index in range(100):
        service_name = service_names[index % len(service_names)]
        timestamp = LOG_START + timedelta(minutes=index * 11)
        level = LOG_LEVELS[index % len(LOG_LEVELS)]
        message = f"{LOG_MESSAGES[index % len(LOG_MESSAGES)]}: {service_name}."
        existing = session.scalar(
            select(LogEntry).where(
                LogEntry.service == service_name,
                LogEntry.timestamp == timestamp,
                LogEntry.message == message,
            )
        )
        if existing is not None:
            summary.skipped += 1
            continue
        session.add(
            LogEntry(
                service=service_name,
                level=level,
                timestamp=timestamp,
                message=message,
            )
        )
        summary.inserted += 1
    session.commit()
    return summary


def print_summary(results: dict[str, SectionSummary]) -> None:
    print("==================================")
    print("WorkShip AI Enterprise Seed")
    print("==================================")
    for name, result in results.items():
        print(f"{name}: {result.inserted} inserted, {result.skipped} skipped")
    print("Seed completed successfully.")


def run_seed() -> None:
    initialize_database()
    session = SessionLocal()
    try:
        team_result, teams = seed_teams(session)
        employee_result = seed_employees(session, teams)
        service_result, services = seed_services(session, teams)
        document_result = seed_documents(session)
        incident_result = seed_incidents(session, teams, services)
        meeting_result = seed_meetings(session)
        log_result = seed_log_entries(session)
        print_summary(
            {
                "Teams": team_result,
                "Employees": employee_result,
                "Services": service_result,
                "Documents": document_result,
                "Incidents": incident_result,
                "Meetings": meeting_result,
                "Log Entries": log_result,
            }
        )
    except SQLAlchemyError as error:
        session.rollback()
        raise SystemExit(f"Seed failed: {error}") from error
    finally:
        session.close()


if __name__ == "__main__":
    run_seed()
