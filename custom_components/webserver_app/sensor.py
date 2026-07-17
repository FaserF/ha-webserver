"""Sensor entities for the Webserver App integration."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.network import get_url
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WebserverAppDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Webserver App sensors."""
    coordinator: WebserverAppDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            WebserverAppStatusSensor(coordinator),
            WebserverAppSSLExpirySensor(coordinator),
            WebserverAppSSLDaysSensor(coordinator),
            WebserverAppConnectionsSensor(coordinator),
            WebserverAppRequestsSensor(coordinator),
            WebserverAppLogErrorsSensor(coordinator),
            WebserverAppLogWarningsSensor(coordinator),
            WebserverAppNginxReadingSensor(coordinator),
            WebserverAppNginxWritingSensor(coordinator),
            WebserverAppNginxWaitingSensor(coordinator),
            WebserverAppApacheIdleWorkersSensor(coordinator),
            WebserverAppApacheBytesPerSecSensor(coordinator),
            WebserverAppApacheReqPerSecSensor(coordinator),
            WebserverAppApacheUptimeSensor(coordinator),
        ]
    )


class WebserverAppSensor(
    CoordinatorEntity[WebserverAppDataUpdateCoordinator], SensorEntity
):
    """Base class for Webserver App sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: WebserverAppDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = description
        self.addon_slug = coordinator.addon_slug
        self._attr_unique_id = f"{self.addon_slug}_{description.key}"

        try:
            base_url = get_url(coordinator.hass, require_current_request=False)
            config_url = f"{base_url}/api/hassio_ingress/{self.addon_slug}/"
        except Exception:
            config_url = f"homeassistant://hassio/addon/{self.addon_slug}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.addon_slug)},
            name=self.addon_slug,
            manufacturer="FaserF",
            model=coordinator.data.get("name") or "Apache2/Nginx HA App",
            sw_version=coordinator.data.get("version"),
            configuration_url=config_url,
        )


class WebserverAppStatusSensor(WebserverAppSensor):
    """Status sensor for Webserver App."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="status",
                name="Status",
                icon="mdi:server",
            ),
        )

    @property
    def native_value(self) -> str | None:
        """Return the status of the addon."""
        return self.coordinator.data.get("state")


class WebserverAppSSLExpirySensor(WebserverAppSensor):
    """Sensor for SSL certificate expiry date."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="ssl_expiry",
                name="SSL Expiry",
                device_class=SensorDeviceClass.TIMESTAMP,
                entity_category=EntityCategory.DIAGNOSTIC,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> datetime | None:
        """Return the expiry date."""
        return self.coordinator.data.get("ssl_expiry")

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self.coordinator.data.get("ssl_enabled", False)


class WebserverAppSSLDaysSensor(WebserverAppSensor):
    """Sensor for SSL certificate days remaining."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="ssl_days_remaining",
                name="SSL Days Remaining",
                native_unit_of_measurement=UnitOfTime.DAYS,
                state_class=SensorStateClass.MEASUREMENT,
                entity_category=EntityCategory.DIAGNOSTIC,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return the days remaining."""
        return self.coordinator.data.get("ssl_days_remaining")

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self.coordinator.data.get("ssl_enabled", False)


class WebserverAppConnectionsSensor(WebserverAppSensor):
    """Sensor for active connections."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="active_connections",
                name="Active Connections",
                icon="mdi:account-network",
                state_class=SensorStateClass.MEASUREMENT,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return the number of active connections."""
        return self.coordinator.data.get("active_connections")


class WebserverAppRequestsSensor(WebserverAppSensor):
    """Sensor for total requests."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="total_requests",
                name="Total Requests",
                icon="mdi:cached",
                state_class=SensorStateClass.TOTAL_INCREASING,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return the total number of requests."""
        return self.coordinator.data.get("total_accesses") or self.coordinator.data.get(
            "total_handled_requests"
        )


class WebserverAppLogErrorsSensor(WebserverAppSensor):
    """Sensor for log errors."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="log_errors",
                name="Log Errors",
                icon="mdi:alert-circle",
                state_class=SensorStateClass.MEASUREMENT,
                entity_category=EntityCategory.DIAGNOSTIC,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return the number of errors in logs."""
        return self.coordinator.data.get("log_errors")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {"recent_errors": self.coordinator.data.get("log_errors_list", [])}


class WebserverAppLogWarningsSensor(WebserverAppSensor):
    """Sensor for log warnings."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="log_warnings",
                name="Log Warnings",
                icon="mdi:alert",
                state_class=SensorStateClass.MEASUREMENT,
                entity_category=EntityCategory.DIAGNOSTIC,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return the number of warnings in logs."""
        return self.coordinator.data.get("log_warnings")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {"recent_warnings": self.coordinator.data.get("log_warnings_list", [])}


class WebserverAppNginxReadingSensor(WebserverAppSensor):
    """Sensor for Nginx reading connections."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="nginx_reading",
                name="Nginx Reading Connections",
                icon="mdi:arrow-down-bold",
                state_class=SensorStateClass.MEASUREMENT,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return reading connections."""
        return self.coordinator.data.get("nginx_reading")

    @property
    def available(self) -> bool:
        """Return True if Nginx is running and connection details are available."""
        return (
            super().available
            and self.coordinator.data.get("webserver_type") == "nginx"
            and "nginx_reading" in self.coordinator.data
        )


class WebserverAppNginxWritingSensor(WebserverAppSensor):
    """Sensor for Nginx writing connections."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="nginx_writing",
                name="Nginx Writing Connections",
                icon="mdi:arrow-up-bold",
                state_class=SensorStateClass.MEASUREMENT,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return writing connections."""
        return self.coordinator.data.get("nginx_writing")

    @property
    def available(self) -> bool:
        """Return True if Nginx is running and connection details are available."""
        return (
            super().available
            and self.coordinator.data.get("webserver_type") == "nginx"
            and "nginx_writing" in self.coordinator.data
        )


class WebserverAppNginxWaitingSensor(WebserverAppSensor):
    """Sensor for Nginx waiting connections."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="nginx_waiting",
                name="Nginx Waiting Connections",
                icon="mdi:clock-outline",
                state_class=SensorStateClass.MEASUREMENT,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return waiting connections."""
        return self.coordinator.data.get("nginx_waiting")

    @property
    def available(self) -> bool:
        """Return True if Nginx is running and connection details are available."""
        return (
            super().available
            and self.coordinator.data.get("webserver_type") == "nginx"
            and "nginx_waiting" in self.coordinator.data
        )


class WebserverAppApacheIdleWorkersSensor(WebserverAppSensor):
    """Sensor for Apache idle workers."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="apache_idle_workers",
                name="Apache Idle Workers",
                icon="mdi:account-network-outline",
                state_class=SensorStateClass.MEASUREMENT,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return idle workers."""
        return self.coordinator.data.get("apache_idle_workers")

    @property
    def available(self) -> bool:
        """Return True if Apache is running and idle worker details are available."""
        return (
            super().available
            and self.coordinator.data.get("webserver_type") == "apache"
            and "apache_idle_workers" in self.coordinator.data
        )


class WebserverAppApacheBytesPerSecSensor(WebserverAppSensor):
    """Sensor for Apache transfer rate."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="apache_bytes_per_sec",
                name="Apache Throughput",
                icon="mdi:transfer",
                native_unit_of_measurement="B/s",
                state_class=SensorStateClass.MEASUREMENT,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> float | None:
        """Return transfer rate in bytes per second."""
        return self.coordinator.data.get("apache_bytes_per_sec")

    @property
    def available(self) -> bool:
        """Return True if Apache is running and transfer rate is available."""
        return (
            super().available
            and self.coordinator.data.get("webserver_type") == "apache"
            and "apache_bytes_per_sec" in self.coordinator.data
        )


class WebserverAppApacheReqPerSecSensor(WebserverAppSensor):
    """Sensor for Apache request rate."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="apache_req_per_sec",
                name="Apache Request Rate",
                icon="mdi:speedometer",
                native_unit_of_measurement="req/s",
                state_class=SensorStateClass.MEASUREMENT,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> float | None:
        """Return request rate."""
        return self.coordinator.data.get("apache_req_per_sec")

    @property
    def available(self) -> bool:
        """Return True if Apache is running and request rate is available."""
        return (
            super().available
            and self.coordinator.data.get("webserver_type") == "apache"
            and "apache_req_per_sec" in self.coordinator.data
        )


class WebserverAppApacheUptimeSensor(WebserverAppSensor):
    """Sensor for Apache server uptime."""

    def __init__(self, coordinator: WebserverAppDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            SensorEntityDescription(
                key="apache_uptime",
                name="Apache Uptime",
                icon="mdi:clock-start",
                native_unit_of_measurement=UnitOfTime.SECONDS,
                state_class=SensorStateClass.MEASUREMENT,
                entity_registry_enabled_default=False,
            ),
        )

    @property
    def native_value(self) -> int | None:
        """Return uptime in seconds."""
        return self.coordinator.data.get("apache_uptime")

    @property
    def available(self) -> bool:
        """Return True if Apache is running and uptime is available."""
        return (
            super().available
            and self.coordinator.data.get("webserver_type") == "apache"
            and "apache_uptime" in self.coordinator.data
        )
