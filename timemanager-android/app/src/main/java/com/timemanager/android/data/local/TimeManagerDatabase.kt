package com.timemanager.android.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.timemanager.android.data.model.Task
import com.timemanager.android.data.model.Schedule
import com.timemanager.android.data.model.Preferences

@Database(
    entities = [Task::class, Schedule::class, Preferences::class],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class TimeManagerDatabase : RoomDatabase() {
    abstract fun taskDao(): TaskDao
    abstract fun scheduleDao(): ScheduleDao
    abstract fun preferencesDao(): PreferencesDao

    companion object {
        @Volatile
        private var INSTANCE: TimeManagerDatabase? = null

        fun getDatabase(context: Context): TimeManagerDatabase {
            return INSTANCE ?: synchronized(this) {
                Room.databaseBuilder(
                    context.applicationContext,
                    TimeManagerDatabase::class.java,
                    "timemanager_db"
                )
                .fallbackToDestructiveMigration()
                .build()
                .also { INSTANCE = it }
            }
        }
    }
}
