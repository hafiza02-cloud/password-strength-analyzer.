
import io
import csv


def create_security_report(result):
    """Create a downloadable CSV report without the password itself."""

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Password Security Analysis Report"])
    writer.writerow(["Score", f"{result['score']}/100"])
    writer.writerow(["Strength", result["strength"]])
    writer.writerow(["Risk Level", result["risk"]])
    writer.writerow([])
    writer.writerow(["Security Check", "Result"])

    for check, passed in result["checks"].items():
        writer.writerow([check, "Passed" if passed else "Needs attention"])

    writer.writerow([])
    writer.writerow(["Recommendations"])

    for recommendation in result["recommendations"]:
        writer.writerow([recommendation])

    return output.getvalue()
