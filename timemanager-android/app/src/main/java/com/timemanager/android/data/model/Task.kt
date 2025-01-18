package com.timemanager.android.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

@Entity(tableName = "tasks")
data class Task(
    @PrimaryKey val id: String,
    val title: String,
    val description: String?,
    val dueDate: Date?,
    val completed: Boolean = false,
    val priority: Int = 0,
    val lastModified: Date = Date(),
    val syncStatus: SyncStatus = SyncStatus.PENDING
)

enum class SyncStatus {
    SYNCED,
    PENDING,
    ERROR
}
