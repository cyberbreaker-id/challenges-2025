// Folder Management Module
class FolderManager {
    constructor() {
        this.selectedFolderId = null;
        this.foldersCache = { temporary: [], database: [] };
    }

    databaseOrTemporary(choice) {
        switch (choice) {
            case "temporary":
                return "temporary";

            case "database":
                return "database";

            default:
                return "temporary";
        }
    }

    async loadFolders(storageType = currentStorageType) {
        try {
            storageType = this.databaseOrTemporary(storageType);
            const response = await fetch(`/folder/api?storage=${storageType}`);
            const foldersRaw = await response.json();

            const folders = foldersRaw.map((item) => {
                if (item.folders) return item.folders;
                return item;
            });

            this.foldersCache[storageType] = folders;

            const foldersList = document.getElementById("foldersList");
            foldersList.innerHTML = "";

            if (folders.length === 0) {
                foldersList.innerHTML = "<p>No folders found. Create one to get started!</p>";
            } else {
                folders.forEach((folder) => {
                    const folderCard = document.createElement("div");
                    folderCard.className = "folder-card";
                    folderCard.dataset.folderId = folder.id;
                    folderCard.onclick = () => this.selectFolder(folder.id, folder.name);
                    folderCard.innerHTML = `
                        <div class="folder-actions">
                            <button class="btn btn-small btn-danger" onclick="event.stopPropagation(); folderManager.deleteFolder(${folder.id}, '${storageType}')">&times;</button>
                        </div>
                        <div class="folder-name">${escapeHtml(folder.name)}</div>
                        <div class="folder-meta">Created: ${escapeHtml(formatDate(folder.createdAt))}</div>
                    `;
                    foldersList.appendChild(folderCard);
                });
            }
        } catch (error) {
            console.error("Error loading folders:", error);
        }
    }

    selectFolder(folderId, folderName) {
        this.selectedFolderId = folderId;

        // Update UI
        document.querySelectorAll(".folder-card").forEach((card) => card.classList.remove("selected"));
        document.querySelector(`[data-folder-id="${folderId}"]`).classList.add("selected");

        // Update form
        document.getElementById("selectedFolderId").value = folderId;
        const storageType = currentStorageType === "temporary" ? "Temporary" : "Database";
        document.getElementById("folderSelection").textContent = `Selected: ${folderName} (${storageType} Storage)`;
        document.getElementById("createBtn").disabled = false;

        // Load notes for this folder
        noteManager.loadNotesForFolder(folderId);
    }

    async deleteFolder(folderId, storageType) {
        storageType = this.databaseOrTemporary(storageType);
        if (confirm("Are you sure? This will delete the folder and all its notes.")) {
            try {
                const response = await fetch(`/folder/${folderId}?storage=${storageType}`, {
                    method: "DELETE",
                });

                if (response.ok) {
                    await this.loadFolders(storageType);
                    document.getElementById("notesList").innerHTML = "";
                    this.selectedFolderId = null;
                    document.getElementById("selectedFolderId").value = "";
                    document.getElementById("folderSelection").textContent = "Select a folder above to continue";
                    document.getElementById("createBtn").disabled = true;
                } else {
                    const errorData = await response.json();
                    alert(errorData.error || "Error deleting folder");
                }
            } catch (error) {
                console.error("Error deleting folder:", error);
            }
        }
    }

    showCreateFolderModal() {
        document.getElementById("folderModal").style.display = "block";
    }

    closeFolderModal() {
        document.getElementById("folderModal").style.display = "none";
        document.getElementById("folderForm").reset();
    }

    async createFolder(folderData) {
        
        try {
            console.log("Creating folder with data:", folderData);
            const response = await fetch("/folder/create", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(folderData),
            });

            console.log("Response status:", response.status);

            if (response.ok) {
                const result = await response.json();
                console.log("Folder created successfully:", result);
                this.closeFolderModal();
                await this.loadFolders(currentStorageType);
            } else {
                const errorData = await response.json();
                console.log("Error response:", errorData);
                alert(errorData.error || "Error creating folder");
            }
        } catch (error) {
            console.error("Error creating folder:", error);
            alert("Error creating folder");
        }
    }

    switchStorage() {
        currentStorageType = document.getElementById("viewStorageType").value;

        // Save selected storage type to localStorage
        localStorage.setItem("selectedStorageType", currentStorageType);

        document.getElementById("folderIsTemporary").checked = currentStorageType === "temporary";

        this.selectedFolderId = null;
        document.getElementById("selectedFolderId").value = "";
        document.getElementById("folderSelection").textContent = "Select a folder above to continue";
        document.getElementById("createBtn").disabled = true;
        document.getElementById("notesList").innerHTML = "";

        this.loadFolders(currentStorageType);
    }
}

// Initialize folder manager
const folderManager = new FolderManager();
