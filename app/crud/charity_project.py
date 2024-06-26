from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, str]]:
        stmt = (
            select(
                CharityProject.name,
                CharityProject.description,
                CharityProject.create_date,
                CharityProject.close_date
            ).where(CharityProject.fully_invested == 1)
        )

        projects = await session.execute(stmt)
        projects = projects.all()

        final_projects = []
        for project in projects:
            time = project.close_date - project.create_date
            final_projects.append(
                {
                    'name': project.name,
                    'description': project.description,
                    'time': time
                }
            )
        return sorted(final_projects, key=lambda p: p['time'])


charity_project_crud = CRUDCharityProject(CharityProject)
