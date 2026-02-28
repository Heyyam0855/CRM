"""GitHub Integration — Services"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class GitHubService:
    """GitHub API ilə işləyən servis."""

    def __init__(self):
        from django.conf import settings
        self.token = getattr(settings, 'GITHUB_TOKEN', '')
        self.org = getattr(settings, 'GITHUB_ORGANIZATION', '')
        self._client = None

    @property
    def client(self):
        if not self._client:
            from github import Github
            self._client = Github(self.token)
        return self._client

    def create_student_repository(
        self,
        repo_name: str,
        student_github_username: str,
        description: str = ''
    ) -> Optional[str]:
        """
        Tələbə üçün private repository yaradır və tələbəyə collaborator hüququ verir.

        Args:
            repo_name: Repository adı
            student_github_username: Tələbənin GitHub istifadəçi adı
            description: Repository açıqlaması

        Returns:
            Optional[str]: Uğurlu olarsa repo URL, əks halda None
        """
        try:
            if self.org:
                org = self.client.get_organization(self.org)
                repo = org.create_repo(
                    name=repo_name,
                    description=description,
                    private=True,
                    auto_init=True
                )
            else:
                user = self.client.get_user()
                repo = user.create_repo(
                    name=repo_name,
                    description=description,
                    private=True,
                    auto_init=True
                )

            # Tələbəyə collaborator icazəsi ver
            if student_github_username:
                repo.add_to_collaborators(student_github_username, permission='push')
                logger.info(
                    f"Collaborator əlavə edildi: {student_github_username} → {repo_name}"
                )

            logger.info(f"GitHub repo yaradıldı: {repo.html_url}")
            return repo.html_url

        except Exception as e:
            logger.error(f"GitHub repo xətası: {e}", exc_info=True)
            return None

    def repo_exists(self, repo_name: str) -> bool:
        """Repository mövcuddurmu yoxlayır."""
        try:
            if self.org:
                org = self.client.get_organization(self.org)
                org.get_repo(repo_name)
            else:
                user = self.client.get_user()
                user.get_repo(repo_name)
            return True
        except Exception:
            return False
