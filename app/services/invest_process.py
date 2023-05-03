from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def make_transaction(session: AsyncSession):
    projects = await CharityProject.get_not_fully_invested(session)
    donations = await Donation.get_not_fully_invested(session)

    while projects and donations:
        project = projects[0]
        donation = donations[0]

        free_money = donation.how_many_we_need_to_close()
        needed_money = project.how_many_we_need_to_close()

        if free_money > needed_money:
            project.mark_as_fully_invested()
            donation.invested_amount += needed_money
            projects.pop(0)

        elif needed_money > free_money:
            donation.mark_as_fully_invested()
            project.invested_amount += free_money
            donations.pop(0)

        else:
            project.mark_as_fully_invested()
            projects.pop(0)
            donation.mark_as_fully_invested()
            donations.pop(0)

        session.add_all([project, donation])

    await session.commit()
