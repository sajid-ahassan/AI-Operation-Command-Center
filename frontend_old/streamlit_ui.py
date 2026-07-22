import streamlit as st
import requests

URL = "http://localhost:8000"

def post_request(endpoint, data):
    response = requests.post(f"{URL}{endpoint}", json=data)
    return response.json()

def get_request(endpoint):
    response = requests.get(f"{URL}{endpoint}")
    return response.json()

# Clean Page Header
st.title("📥 Pending Approvals Dashboard")
st.write("---")

pending_approvals = get_request("/api/panding_approval")

if not pending_approvals:
    st.success("🎉 No pending approvals left!")
else:
    for approval in pending_approvals:
        # A clean, single-line header for the dropdown
        header = f"📋 Request from {approval['email_id']} | {approval['category']} ({approval['priority']} Priority)"
        
        with st.expander(header):
            # Split metadata into two clean columns
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown(f"**Action Required:** `{approval['action']}`")
                st.markdown(f"**Reason:** {approval['reason']}")
            with col_right:
                st.markdown(f"**Current Status:** {approval['approval_status']}")
            
            st.write("---")
            
            # Use a blockquote format for the email body text to make it stand out
            st.markdown("**Email Body:**")
            st.markdown(f"> {approval['body']}")
            
            st.write("")
            
            # Align buttons side-by-side on the left without stretching them too wide
            btn_col1, btn_col2, _ = st.columns([1, 1, 4])
            
            # Available actions
            available_actions = [
                'CREATE_CRM_LEDGER', 'CREATE_SUPPORT_TICKET', 'SCHEDULE_MEETING', 'SEND_QUOTATION','NO_ACTION'
            ]

            available_priorities = [
                "critical",
                "high",
                "medium",
                "low"
            ]


            st.write("---")

            # Human decision controls
            selected_actions = st.multiselect(
                "Select Final Action(s)",
                options=available_actions,
                default=approval["action"] if isinstance(approval["action"], list) else [approval["action"]],
                key=f"action_{approval['id']}"
            )


            selected_priority = st.selectbox(
                "Select Final Priority",
                options=available_priorities,
                index=available_priorities.index(
                    approval["priority"].lower()
                ) if approval["priority"].lower() in available_priorities else 2,
                key=f"priority_{approval['id']}"
            )


            review_note = st.text_area(
                "Reviewer Note",
                placeholder="Why are you approving or modifying this request?",
                key=f"note_{approval['id']}"
            )


            st.write("")


            btn_col1, btn_col2, _ = st.columns([1, 1, 4])


            with btn_col1:
                if st.button(
                    "Approve",
                    key=f"app_{approval['id']}",
                    use_container_width=True
                ):

                    payload = {
                        "action": selected_actions,
                        "priority": selected_priority,
                        "note": review_note
                    }

                    result = post_request(
                        f"/api/approve/{approval['id']}",
                        payload
                    )

                    st.success(
                        f"Request {approval['id']} Approved"
                    )

                    st.rerun()


            with btn_col2:
                if st.button(
                    "Reject",
                    key=f"rej_{approval['id']}",
                    type="primary",
                    use_container_width=True
                ):

                    payload = {
                        "note": review_note
                    }

                    result = post_request(
                        f"/api/reject/{approval['id']}",
                        payload
                    )

                    st.error(
                        f"Request {approval['id']} Rejected"
                    )

                    st.rerun()