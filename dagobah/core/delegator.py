import logging

from ..backend.base import BaseBackend

logger = logging.getLogger('dagobah')

class CommitDelegator(object):
    """
    The CommitDelegator is a class designed to handle any and all commits
    to the database.

    The delegator takes in commit requests from various objects, and decides
    if they should actually be committed, and if so, manage any special
    processing.
    """

    def __init__(self, backend):
        self.backend = backend

    def commit_dagobah(self, dagobah, cascade=False):
        """ Commit this Dagobah instance to the backend.

        If cascade is True, all child Jobs are commited as well.
        """
        logger.debug('Committing Dagobah instance with cascade={0}'.
                     format(cascade))
        if cascade:
            [self.commit_job(job, False) for job in dagobah.jobs]
        self.backend.commit_dagobah(dagobah._serialize())

    def commit_job(self, job, commit_dagobah=True):
        """ Store metadata on this Job to the backend. """
        logger.debug('Committing job {0}'.format(job.name))
        self.backend.commit_job(job._serialize())
        if commit_dagobah:
            self.commit_dagobah(job.parent)

    def commit_run_log(self, job):
        """" Commit the current run log to the backend. """
        logger.debug('Committing run log for job {0}'.format(job.name))
        self.backend.commit_log(job.run_log)
