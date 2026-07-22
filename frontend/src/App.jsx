import { useEffect, useState } from "react";
import {
  BrainCircuit,
  CheckCircle,
  XCircle,
  Activity,
  ShieldCheck,
} from "lucide-react";

const API = "http://127.0.0.1:8000";

const actions = [
  "CREATE_CRM_LEDGER",
  "CREATE_SUPPORT_TICKET",
  "SCHEDULE_MEETING",
  "SEND_QUOTATION",
  "NO_ACTION",
];

const priorities = ["critical", "high", "medium", "low"];

function ApprovalCard({ item, reload }) {
  const [action, setAction] = useState(
    Array.isArray(item.action) ? item.action : [],
  );

  const [priority, setPriority] = useState(item.priority || "medium");

  const [note, setNote] = useState("");

  async function approve() {
    try {
      await fetch(`${API}/api/approve/${item.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action,
          priority,
          note,
        }),
      });

      reload();
    } catch (error) {
      console.error("Approve error:", error);
    }
  }

  async function reject() {
    try {
      await fetch(`${API}/api/reject/${item.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          note,
        }),
      });

      reload();
    } catch (error) {
      console.error("Reject error:", error);
    }
  }

  return (
    <div className="bg-slate-900/80 border border-slate-700 rounded-3xl p-6 shadow-xl">
      <div className="flex justify-between">
        <div>
          <h2 className="text-xl font-bold">
            {item.sender || "Unknown Sender"}
          </h2>

          <p className="text-slate-400">{item.category || "General"}</p>
        </div>

        <div className="bg-red-500/20 text-red-300 px-4 py-2 rounded-full">
          {item.priority}
        </div>
      </div>

      <div className="mt-5 grid md:grid-cols-2 gap-5">
        <div className="bg-blue-500/10 p-4 rounded-xl">
          <h3 className="font-bold">AI Action</h3>

          <p>
            {Array.isArray(item.action) ? item.action.join(", ") : item.action}
          </p>
        </div>

        <div className="bg-purple-500/10 p-4 rounded-xl">
          <h3 className="font-bold">Reason</h3>

          <p>{item.reason || "No reason"}</p>
        </div>
      </div>

      <div className="mt-5">
        <h3 className="font-bold">Email</h3>

        <div className="bg-black/40 rounded-xl p-4 mt-2 whitespace-pre-wrap">
          {item.body}
        </div>
      </div>

      <div className="mt-5 space-y-3">
        <div className="bg-slate-800 rounded-xl p-4">
          <p className="font-bold mb-3">Select Final Actions</p>

          <div className="space-y-2">
            {actions.map((a) => (
              <label key={a} className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={action.includes(a)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setAction([...action, a]);
                    } else {
                      setAction(action.filter((x) => x !== a));
                    }
                  }}
                  className="w-4 h-4"
                />

                <span>{a}</span>
              </label>
            ))}
          </div>
        </div>

        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          className="w-full bg-slate-800 p-3 rounded-xl"
        >
          {priorities.map((p) => (
            <option key={p}>{p}</option>
          ))}
        </select>

        <textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Reviewer note"
          className="w-full bg-slate-800 p-3 rounded-xl"
        />
      </div>

      <div className="flex gap-4 mt-5">
        <button
          onClick={approve}
          className="flex-1 bg-green-600 p-3 rounded-xl flex justify-center gap-2"
        >
          <CheckCircle />
          Approve
        </button>

        <button
          onClick={reject}
          className="flex-1 bg-red-600 p-3 rounded-xl flex justify-center gap-2"
        >
          <XCircle />
          Reject
        </button>
      </div>
    </div>
  );
}

export default function App() {
  const [items, setItems] = useState([]);

  const [error, setError] = useState("");

  async function load() {
    console.log("LOAD STARTED");

    try {
      const response = await fetch(`${API}/api/panding_approval`);

      console.log("STATUS:", response.status);

      const data = await response.json();

      console.log("BACKEND DATA:", data);

      setItems(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("API ERROR:", error);

      setError(error.message);
    }
  }

  useEffect(() => {
    console.log("APP LOADED");

    load();
  }, []);

  return (
    <div className="max-w-7xl mx-auto p-8">
      <header className="mb-16">
        <div className="flex gap-4 items-center">
          <BrainCircuit size={45} />

          <h1 className="text-5xl font-bold">AI Operations Command Center</h1>
        </div>

        <p className="text-slate-400 mt-4 text-xl">
          AI powered email intelligence, human approval, and automated business
          workflows.
        </p>
      </header>

      <section className="grid md:grid-cols-3 gap-5 mb-16">
        <div className="bg-slate-900 p-6 rounded-3xl">
          <Activity />
          <h2 className="font-bold mt-3">AI Decision Engine</h2>
        </div>

        <div className="bg-slate-900 p-6 rounded-3xl">
          <ShieldCheck />
          <h2 className="font-bold mt-3">Human Oversight</h2>
        </div>

        <div className="bg-slate-900 p-6 rounded-3xl">
          <BrainCircuit />
          <h2 className="font-bold mt-3">Workflow Automation</h2>
        </div>
      </section>

      <section>
        <h2 className="text-3xl font-bold mb-6">Pending Approvals</h2>

        {error && <div className="bg-red-900 p-4 rounded-xl">{error}</div>}

        {items.length === 0 ? (
          <div className="bg-green-900/30 border border-green-700 p-8 rounded-3xl">
            <h3 className="text-2xl font-bold">System Clear</h3>

            <p>No pending human approvals.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {items.map((item) => (
              <ApprovalCard
                key={item.id || item.email_id}
                item={item}
                reload={load}
              />
            ))}
          </div>
        )}
      </section>

      <footer className="mt-20 text-slate-400">
        Built with LangGraph • FastAPI • React • n8n • HubSpot
      </footer>
    </div>
  );
}
