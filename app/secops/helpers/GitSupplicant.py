import os
import shutil
import tempfile
import time
from git import Repo

from secops.helpers.Log import Log


class GitSupplicant:
    def __init__(self, asset: dict, **kwargs):
        self.asset: dict = asset
        self.sshCmd: str = ""
        self.remote: str = ""
        self.tmpLocal: str = ""
        self.tmpRepoKeyFile: str = ""
        self.tmpUserPrivateKeyFile: str = ""

        self.__init(**kwargs)
        self.__clone()



    def __del__(self):
        try:
            shutil.rmtree(self.tmpLocal)

            os.remove(self.tmpRepoKeyFile)
            os.remove(self.tmpUserPrivateKeyFile)
        except OSError:
            pass



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def getLocalRepo(self) -> str:
        return self.tmpLocal



    def pull(self, origin: str = "origin", rebase: bool = False):
        Log.actionLog(f"[GIT Supplicant] Pulling from {self.remote}")

        try:
            repo = Repo(self.tmpLocal)

            with repo.git.custom_environment(GIT_SSH_COMMAND=self.sshCmd):
                origin = repo.remote(name=origin)
                origin.pull(rebase=rebase)
        except Exception as e:
            raise e



    def commit(self, commitMessage: str = "Automated commit"):
        Log.actionLog(f"[GIT Supplicant] Committing files")

        try:
            repo = Repo(self.tmpLocal)

            repo.git.add(all=True)
            repo.index.commit(commitMessage)
        except Exception as e:
            raise e



    def push(self, origin: str = "origin"):
        Log.actionLog(f"[GIT Supplicant] Pushing to {self.remote}")

        try:
            repo = Repo(self.tmpLocal)

            with repo.git.custom_environment(GIT_SSH_COMMAND=self.sshCmd):
                origin = repo.remote(name=origin)
                origin.pull(rebase=True)
                origin.push()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __init(self, **kwargs):
        try:
            # Temporarily save private key in a file.
            self.tmpUserPrivateKeyFile = f"{tempfile.NamedTemporaryFile().name}_userkey"
            with open(self.tmpUserPrivateKeyFile, mode="w", opener=lambda p, fl: os.open(p, fl, 0o400)) as f:
                f.write(self.asset.get("userkey", ""))

            # Temporarily save host public key in a file.
            self.tmpRepoKeyFile = f"{tempfile.NamedTemporaryFile().name}_repokey"
            with open(self.tmpRepoKeyFile, mode="w", opener=lambda p, fl: os.open(p, fl, 0o400)) as f:
                f.write(self.asset.get("repokey", ""))

            # Create a temp folder for local git repo.
            with tempfile.TemporaryDirectory() as self.tmpLocal:
                pass

            # Define properties.
            self.sshCmd = "ssh -i %s -o UserKnownHostsFile=%s -o IdentitiesOnly=yes" % (self.tmpUserPrivateKeyFile, self.tmpRepoKeyFile)
            self.remote = self.asset.get("baseurl", "")
        except Exception as e:
            raise e



    def __clone(self):
        try:
            Log.actionLog(f"[GIT Supplicant] Cloning {self.remote}")

            Repo.clone_from(self.remote, self.tmpLocal, env={"GIT_SSH_COMMAND": self.sshCmd})
            time.sleep(10)
        except Exception as e:
            raise e
