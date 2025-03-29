return {
  -- {
  --   "https://gitlab.com/itaranto/plantuml.nvim",
  --   version = "*",
  --   config = function()
  --     require("plantuml").setup()
  --   end,
  -- },
  -- {
  --   "scrooloose/vim-slumlord",
  --   -- Puedes añadir opciones de configuración aquí si lo necesitas
  -- },
  {
    "aklt/plantuml-syntax",
    -- Puedes añadir opciones de configuración aquí si lo necesitas
  },
  {
    "tyru/open-browser.vim",
    -- Puedes añadir opciones de configuración aquí si lo necesitas
  },
  {
    "previm/previm",
    config = function()
      vim.g.previm_open_browser = false -- Evita que se abra el navegador
      vim.g.previm_command = "plantuml -tsvg -o %:t:r.svg %" -- Comando para PlantUML
    end,
  },
}
