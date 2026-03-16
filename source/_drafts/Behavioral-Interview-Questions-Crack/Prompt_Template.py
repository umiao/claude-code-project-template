


Prefix = "You are a software engineering with search science - relevance team. "


Question = """
How do you ensure effective communication within your team?
"""

Answer = """
Situation: In my previous role, our team struggled with communication, resulting in misunderstandings and project delays.

Task: My objective was to improve communication and ensure everyone was aligned on project progress.

Action: To address this, I leveraged a progress tracking tool called Airflow, introduced by our senior director. I set up regular "prediction market" meetings, where team members could share their goals and estimate the likelihood of achieving them. This approach fostered open dialogue and accountability. Additionally, I initiated stand-up meetings for quick updates and conducted one-on-one check-ins to address individual concerns and challenges.

Result: These initiatives significantly improved team collaboration, resulting in a 30% reduction in project delays. The combination of Airflow and prediction market meetings created a more engaged team atmosphere, ultimately enhancing our productivity and project outcomes.
"""


FirstSolving = """
Suppose you are a seasoned professional candidate for a Meta E6 software engineer position, can you give an sample answer to question “%s” Please make it short and concise, natural and appealing in 160 words, no hard words. A little bit formal. Please use the STAR strategy.
""" % Question

Polish = """
Suppose you are a seasoned professional candidate for a Meta E6 software engineer position, can you polish this answer to question “%s” Please make it short and concise, natural and appealing in 160 words, no hard words, easy to follow. A little bit formal. Please use the STAR strategy. “%s”
""" % (Question, Answer)

Review = """
Suppose you’re a seasoned interviewer at Meta, is this answer to the question “%s” a good one for an E6 candidate? Will it have a negative impression? How to improve it? “%s”
""" % (Question, Answer)








if __name__ == '__main__':

    print(FirstSolving)
    print(Polish)
    print(Review)