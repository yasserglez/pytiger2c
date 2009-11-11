git filter-branch --commit-filter '
        if [ "$GIT_COMMITTER_NAME" = "gnuaha7" ];
        then
                GIT_COMMITTER_NAME="Ariel Hernández Amador";
                GIT_AUTHOR_NAME="Ariel Hernández Amador";
                GIT_COMMITTER_EMAIL="gnuaha7@uh.cu";
                GIT_AUTHOR_EMAIL="gnuaha7@uh.cu";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD
