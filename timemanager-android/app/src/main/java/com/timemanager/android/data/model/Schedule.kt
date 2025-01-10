package com.timemanager.android.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

@Entity(tableName = "schedules")
data class Schedule(
    @PrimaryKey val id: String,
    val title: String,
    val startTime: Date,
    val endTime: Date,
    val description: String?,
    val lastModified: Date = Date(),
    val syncStatus: SyncStatus = SyncStatus.PENDING
)
