"""Unit tests for Webserver App config flow and diagnostics."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import device_registry as dr
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.webserver_app.config_flow import (
    WebserverAppConfigFlow,
    WebserverAppOptionsFlowHandler,
)
from custom_components.webserver_app.const import CONF_ADDON_SLUG, CONF_PORT, DOMAIN
from custom_components.webserver_app.diagnostics import (
    async_get_config_entry_diagnostics,
)


async def test_config_flow_user_and_options_forms(hass: HomeAssistant) -> None:
    """Verify user and options flows render forms cleanly without errors."""
    mock_resp = MagicMock()
    mock_resp.status = 401
    mock_session = MagicMock()
    mock_session.get = AsyncMock(return_value=mock_resp)

    flow = WebserverAppConfigFlow()
    flow.hass = hass

    with (
        patch(
            "custom_components.webserver_app.config_flow.get_supervisor_token",
            return_value="test-token",
        ),
        patch(
            "custom_components.webserver_app.config_flow.async_get_clientsession",
            return_value=mock_session,
        ),
    ):
        result = await flow.async_step_user()

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["data_schema"] is not None

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_ADDON_SLUG: "apache2", CONF_PORT: 80},
        options={"update_interval": 15},
    )
    entry.add_to_hass(hass)

    options_flow = WebserverAppOptionsFlowHandler()
    options_flow.hass = hass
    options_flow.handler = entry.entry_id
    opt_result = await options_flow.async_step_init()

    assert opt_result["type"] == FlowResultType.FORM
    assert opt_result["step_id"] == "init"
    assert opt_result["data_schema"] is not None


async def test_diagnostics_uses_device_registry_helper(hass: HomeAssistant) -> None:
    """Verify diagnostics lists devices for the config entry across HA versions."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_ADDON_SLUG: "apache2", CONF_PORT: 80, "token": "secret"},
        options={},
    )
    entry.add_to_hass(hass)

    dev_reg = dr.async_get(hass)
    dev_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, "apache2")},
        name="Apache2",
        manufacturer="FaserF",
        model="Webserver App",
        sw_version="3.4.14",
    )

    diag = await async_get_config_entry_diagnostics(hass, entry)

    assert diag["config_entry"]["data"]["token"] == "**REDACTED**"
    assert len(diag["registry_debug"]["devices"]) == 1
    assert diag["registry_debug"]["devices"][0]["name"] == "Apache2"
