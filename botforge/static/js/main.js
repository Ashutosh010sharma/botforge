document.addEventListener(
    "DOMContentLoaded",
    function(){

       

    }
);
// ===============================
// Profile Panel
// ===============================

(function () {

    const trigger = document.getElementById("profileTrigger");
    const overlay = document.getElementById("profileOverlay");
    const panel = document.getElementById("profilePanel");
    const closeBtn = document.getElementById("profileClose");

    // If profile doesn't exist on this page
    if (!trigger || !overlay || !panel || !closeBtn) return;

    let profileLoaded = false;

    function openPanel() {

        overlay.classList.add("is-active");
        panel.classList.add("is-active");
        trigger.classList.add("is-open");

        panel.setAttribute("aria-hidden", "false");

        document.body.classList.add("profile-panel-open");

        loadProfile(profileLoaded);

    }

    function closePanel() {

        overlay.classList.remove("is-active");
        panel.classList.remove("is-active");
        trigger.classList.remove("is-open");

        panel.setAttribute("aria-hidden", "true");

        document.body.classList.remove("profile-panel-open");

    }

    trigger.addEventListener("click", openPanel);

    closeBtn.addEventListener("click", closePanel);

    overlay.addEventListener("click", closePanel);

    document.addEventListener("keydown", function (e) {

        if (e.key === "Escape" && panel.classList.contains("is-active")) {

            closePanel();

        }

    });

    function loadProfile(alreadyLoaded = false) {

        if (alreadyLoaded) return;

        $.ajax({

            url: PROFILE_DETAILS_URL,

            type: "GET",

            success: function (response) {

                if (!response.status) return;

                let p = response.data;

                $("#navbarProfileAvatar").text(p.avatar);

                $("#profileAvatar").text(p.avatar);

                $("#profileName").text(p.full_name);

                $("#profileUsername").text("@" + p.username);

                $("#profileMemberSince").text(p.member_since);

                $("#profileFullName").text(p.full_name);

                $("#profileUserName").text(p.username);

                $("#profileEmailAddress").text(p.email);

                $("#profileEmailStatus").text(
                    p.email_verified ? "Verified" : "Not Verified"
                );

                $("#profileAccountStatus").text(p.account_status);

                $("#profileJoined").text(p.member_since);

                $("#profilePlan").text(p.current_plan);

                $("#profileWorkspace").text(p.workspace);

                $("#profileLastLogin").text(p.last_login);

                profileLoaded = true;

            },

            error: function () {

                console.log("Unable to load profile.");

            }

        });

    }

})();