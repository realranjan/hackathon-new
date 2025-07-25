import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const AdminUsersPanel = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({ email: "", password: "", role: "viewer" });
  const [editId, setEditId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState({ username: "", password: "" });

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/admin/users/`);
      const data = await res.json();
      setUsers(data.users || []);
    } catch (e) {
      setError("Failed to fetch users");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleCreate = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/admin/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || data.error || "Failed to create user");
      } else {
        setForm({ email: "", password: "", role: "viewer" });
        fetchUsers();
      }
    } catch (e) {
      setError("Failed to create user");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (user: any) => {
    setEditId(user.id);
    setEditForm({ username: user.email, password: "" });
  };

  const handleUpdate = async () => {
    if (!editId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/admin/users/${editId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editForm)
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || data.error || "Failed to update user");
      } else {
        setEditId(null);
        setEditForm({ username: "", password: "" });
        fetchUsers();
      }
    } catch (e) {
      setError("Failed to update user");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/admin/users/${id}`, {
        method: "DELETE"
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || data.error || "Failed to delete user");
      } else {
        fetchUsers();
      }
    } catch (e) {
      setError("Failed to delete user");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="card-maritime mt-4">
      <CardHeader>
        <CardTitle>Admin User Management</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <h4 className="font-medium mb-2">Create User</h4>
          <div className="flex gap-2 mb-2">
            <Input placeholder="Email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} />
            <Input placeholder="Password" type="password" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} />
            <Input placeholder="Role" value={form.role} onChange={e => setForm(f => ({ ...f, role: e.target.value }))} />
            <Button onClick={handleCreate} disabled={loading}>Create</Button>
          </div>
        </div>
        <div>
          <h4 className="font-medium mb-2">Users</h4>
          <table className="w-full text-xs border">
            <thead>
              <tr>
                <th className="border px-2">ID</th>
                <th className="border px-2">Email</th>
                <th className="border px-2">Role</th>
                <th className="border px-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td className="border px-2">{user.id}</td>
                  <td className="border px-2">{user.email}</td>
                  <td className="border px-2">{user.role}</td>
                  <td className="border px-2">
                    <Button size="sm" variant="outline" onClick={() => handleEdit(user)} disabled={loading}>Edit</Button>
                    <Button size="sm" variant="destructive" onClick={() => handleDelete(user.id)} disabled={loading} className="ml-2">Delete</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {editId && (
          <div className="mt-4">
            <h4 className="font-medium mb-2">Edit User</h4>
            <div className="flex gap-2 mb-2">
              <Input placeholder="Username" value={editForm.username} onChange={e => setEditForm(f => ({ ...f, username: e.target.value }))} />
              <Input placeholder="Password" type="password" value={editForm.password} onChange={e => setEditForm(f => ({ ...f, password: e.target.value }))} />
              <Button onClick={handleUpdate} disabled={loading}>Update</Button>
              <Button onClick={() => setEditId(null)} variant="outline" disabled={loading}>Cancel</Button>
            </div>
          </div>
        )}
        {error && <div className="text-red-500 mt-2">{error}</div>}
      </CardContent>
    </Card>
  );
};

export default AdminUsersPanel; 