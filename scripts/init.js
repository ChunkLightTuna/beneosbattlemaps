  const adventureName = 'Beneos Battlemaps';
  const moduleName = 'beneosbattlemaps';

  /**
   * welcomeJournal (if set) will automatically be imported and opened after the first activation of a
   * scene imported from the module compendium.
   * The name here corresponds to a Journal entry in your compendium and must match exactly (it is case
   * sensitive).
   * Set to the following to disable:
   *   const welcomeJournal = '';
   */
  const welcomeJournal = '';
  /**
   * additionalJournals will automatically be imported. This is a list of Journals by name that should
   * also be imported.
   * Set to the following to disable:
   *   const additionalJournals = [];
   */
  const additionalJournals = [];
  /**
   * additionalMacros will automatically be imported. Each name must match exactly and are case sensitive.
   * Set to the following to disable:
   *   const additionalMacros = [];
   */
  const additionalMacros = [];
  /**
   * creaturePacks is a list of compendium packs to look in for Actors by name (in prioritised order).
   * If the creature is not found in the first pack, it will search through each subsequent pack.
   * The first entry here assumes that you have an Actor pack in your module with the "name" of "actors".
   * The second entry here lists the DnD5e SRD Monsters compendium that comes with the DnD5e system. Feel
   * free to delete the 'dnd5e.monsters' reference if you want, or swapping it to any other system compendium
   * reference.
   * Set to the following to disable:
   *   const creaturePacks = [];
   */
  const creaturePacks = [`${moduleName}.beneos-battlemaps-npcs`, 'dnd5e.monsters'];
  /**
   * journalPacks is a list of compendium packs to look in for Journals by name (in prioritised order).
   * The first entry here assumes that you have a Journal pack in your module with the "name" of "journals".
   * Set to the following to disable:
   *   const journalPacks = [];
   */
  const journalPacks = [`${moduleName}.beneosbattlemaps_journal`];
  /**
   * macroPacks is a list of compendium packs to look in for Macros by name (in prioritised order).
   * The first entry here assumes that you have a Macro pack in your module with the "name" of "macros".
   * Set to the following to disable:
   *   const macroPacks = [];
   */
  const macroPacks = [];
  /**
   * playlistPacks is a list of compendium packs to look in for Playlists by name (in prioritised order).
   * The first entry here assumes that you have a Playlist pack in your module with the "name" of "playlists".
   * Set to the following to disable:
   *   const playlistPacks = [];
   */
  const playlistPacks = [];

  Hooks.once('scenePackerReady', ScenePacker => {
    // Initialise the Scene Packer with your adventure name and module name
    let packer = ScenePacker.Initialise({
      adventureName,
      moduleName,
      creaturePacks,
      journalPacks,
      macroPacks,
      playlistPacks,
      welcomeJournal,
      additionalJournals,
      additionalMacros,
      allowImportPrompts: true, // Set to false if you don't want the initial popup
    });
  });
  
  Hooks.on('ready', async () => {
  if (!game.user.isGM) {
    return;
  }

  const journalName = '_Installation';

  if (game.journal.getName(journalName)) {
    // Already imported
    return;
  }

  const pack = game.packs.get('beneosbattlemaps.beneosbattlemaps_journal');
  const j = pack.index.getName(journalName)
  if (!j) {
    // Journal with that name not found in the compendium pack
    return;
  }

  let journal;
  if (!isNewerVersion('0.8.0', game.data.version)) {
    journal = await game.journal.importFromCompendium(pack, j._id);
  } else {
    journal = await game.journal.importFromCollection('beneosbattlemaps.beneosbattlemaps_journal', j._id);
  }

  if (journal) {
    journal.sheet.render(true);
  }
}
)
;