package com.timemanager.android.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

@Entity(tableName = "preferences")
data class Preferences(
    @PrimaryKey val id: String = "user_preferences",
    val language: String = "en",
    val theme: String = "light",
    val syncInterval: Long = 300000, // 5 minutes in milliseconds
    val lastModified: Date = Date(),
    val syncStatus: SyncStatus = SyncStatus.PENDING
)
