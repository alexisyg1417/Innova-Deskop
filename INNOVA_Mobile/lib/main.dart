import 'package:flutter/material.dart';

void main() {
  runApp(const InnovaMobileApp());
}

class Property {
  final String title;
  final String location;
  final int price;
  final String operation;
  final int bedrooms;
  final int bathrooms;
  final int parking;

  const Property({
    required this.title,
    required this.location,
    required this.price,
    required this.operation,
    required this.bedrooms,
    required this.bathrooms,
    required this.parking,
  });
}

const properties = [
  Property(
    title: 'Casa Familiar Cholula',
    location: 'San Pedro Cholula, Puebla',
    price: 3250000,
    operation: 'Venta',
    bedrooms: 4,
    bathrooms: 2,
    parking: 2,
  ),
  Property(
    title: 'Residencia La Paz',
    location: 'La Paz, Puebla',
    price: 25000,
    operation: 'Renta',
    bedrooms: 5,
    bathrooms: 3,
    parking: 2,
  ),
  Property(
    title: 'Departamento Angelópolis',
    location: 'Angelópolis, Puebla',
    price: 1850000,
    operation: 'Venta',
    bedrooms: 2,
    bathrooms: 2,
    parking: 1,
  ),
];

class InnovaMobileApp extends StatelessWidget {
  const InnovaMobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    const navy = Color(0xFF172B3A);
    const gold = Color(0xFFC7A052);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'INNOVA Mobile',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: navy,
          primary: navy,
          secondary: gold,
          surface: const Color(0xFFF7F7F5),
        ),
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF7F7F5),
        cardTheme: const CardThemeData(
          elevation: 0,
          margin: EdgeInsets.zero,
        ),
      ),
      home: const MainShell(),
    );
  }
}

class MainShell extends StatefulWidget {
  const MainShell({super.key});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int index = 0;
  final favorites = <String>{};

  @override
  Widget build(BuildContext context) {
    final pages = [
      HomePage(
        favorites: favorites,
        onToggleFavorite: toggleFavorite,
        onOpenCatalog: () => setState(() => index = 1),
      ),
      CatalogPage(
        favorites: favorites,
        onToggleFavorite: toggleFavorite,
      ),
      const AppointmentsPage(),
      FavoritesPage(
        favorites: favorites,
        onToggleFavorite: toggleFavorite,
      ),
    ];

    return Scaffold(
      body: IndexedStack(index: index, children: pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (value) => setState(() => index = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Inicio'),
          NavigationDestination(icon: Icon(Icons.apartment_outlined), selectedIcon: Icon(Icons.apartment), label: 'Catálogo'),
          NavigationDestination(icon: Icon(Icons.calendar_month_outlined), selectedIcon: Icon(Icons.calendar_month), label: 'Citas'),
          NavigationDestination(icon: Icon(Icons.favorite_border), selectedIcon: Icon(Icons.favorite), label: 'Favoritos'),
        ],
      ),
    );
  }

  void toggleFavorite(Property property) {
    setState(() {
      if (!favorites.add(property.title)) {
        favorites.remove(property.title);
      }
    });
  }
}

class BrandedAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  const BrandedAppBar({super.key, this.title = 'INNOVA'});

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white,
      surfaceTintColor: Colors.white,
      title: Row(
        children: [
          const Icon(Icons.apartment_rounded),
          const SizedBox(width: 8),
          Text(title, style: const TextStyle(fontWeight: FontWeight.w800, letterSpacing: 2)),
        ],
      ),
      actions: [
        IconButton(onPressed: () {}, icon: const Icon(Icons.notifications_none)),
        const Padding(
          padding: EdgeInsets.only(right: 12),
          child: CircleAvatar(child: Icon(Icons.person_outline)),
        ),
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}

class HomePage extends StatelessWidget {
  final Set<String> favorites;
  final void Function(Property) onToggleFavorite;
  final VoidCallback onOpenCatalog;

  const HomePage({
    super.key,
    required this.favorites,
    required this.onToggleFavorite,
    required this.onOpenCatalog,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const BrandedAppBar(),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(18, 18, 18, 30),
        children: [
          Container(
            padding: const EdgeInsets.all(22),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [Color(0xFF233746), Color(0xFF6F7C85)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(28),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('INNOVA LA DIRECCIÓN DE TUS SUEÑOS', style: TextStyle(color: Colors.amber.shade300, fontSize: 12, letterSpacing: 1.5)),
                const SizedBox(height: 10),
                const Text('Encuentra tu próximo hogar.', style: TextStyle(color: Colors.white, fontSize: 30, fontWeight: FontWeight.w800)),
                const SizedBox(height: 8),
                const Text('Compra o renta propiedades desde tu teléfono.', style: TextStyle(color: Colors.white70, height: 1.4)),
                const SizedBox(height: 18),
                FilledButton.icon(onPressed: onOpenCatalog, icon: const Icon(Icons.search), label: const Text('Explorar catálogo')),
              ],
            ),
          ),
          const SizedBox(height: 24),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Propiedades destacadas', style: TextStyle(fontSize: 21, fontWeight: FontWeight.w800)),
              TextButton(onPressed: onOpenCatalog, child: const Text('Ver todas')),
            ],
          ),
          const SizedBox(height: 12),
          ...properties.take(2).map((property) => Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: PropertyCard(
                  property: property,
                  favorite: favorites.contains(property.title),
                  onFavorite: () => onToggleFavorite(property),
                ),
              )),
        ],
      ),
    );
  }
}

class CatalogPage extends StatefulWidget {
  final Set<String> favorites;
  final void Function(Property) onToggleFavorite;
  const CatalogPage({super.key, required this.favorites, required this.onToggleFavorite});

  @override
  State<CatalogPage> createState() => _CatalogPageState();
}

class _CatalogPageState extends State<CatalogPage> {
  String query = '';
  String operation = 'Todas';

  @override
  Widget build(BuildContext context) {
    final filtered = properties.where((p) {
      final matchesText = p.title.toLowerCase().contains(query.toLowerCase()) || p.location.toLowerCase().contains(query.toLowerCase());
      final matchesOperation = operation == 'Todas' || p.operation == operation;
      return matchesText && matchesOperation;
    }).toList();

    return Scaffold(
      appBar: const BrandedAppBar(title: 'CATÁLOGO'),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(18, 18, 18, 30),
        children: [
          TextField(
            onChanged: (value) => setState(() => query = value),
            decoration: InputDecoration(
              hintText: 'Buscar por zona o propiedad',
              prefixIcon: const Icon(Icons.search),
              filled: true,
              fillColor: Colors.white,
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(18), borderSide: BorderSide.none),
            ),
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            children: ['Todas', 'Venta', 'Renta'].map((item) => ChoiceChip(
              label: Text(item),
              selected: operation == item,
              onSelected: (_) => setState(() => operation = item),
            )).toList(),
          ),
          const SizedBox(height: 20),
          Text('${filtered.length} propiedades', style: const TextStyle(fontWeight: FontWeight.w700)),
          const SizedBox(height: 12),
          ...filtered.map((property) => Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: PropertyCard(
                  property: property,
                  favorite: widget.favorites.contains(property.title),
                  onFavorite: () => widget.onToggleFavorite(property),
                ),
              )),
        ],
      ),
    );
  }
}

class PropertyCard extends StatelessWidget {
  final Property property;
  final bool favorite;
  final VoidCallback onFavorite;
  const PropertyCard({super.key, required this.property, required this.favorite, required this.onFavorite});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => PropertyDetailPage(property: property))),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              height: 150,
              decoration: const BoxDecoration(
                gradient: LinearGradient(colors: [Color(0xFFD7C1A2), Color(0xFF8EA58F)]),
              ),
              child: Stack(
                children: [
                  const Center(child: Icon(Icons.home_work_outlined, size: 74, color: Colors.white70)),
                  Positioned(top: 12, left: 12, child: Chip(label: Text(property.operation))),
                  Positioned(top: 8, right: 8, child: IconButton.filledTonal(onPressed: onFavorite, icon: Icon(favorite ? Icons.favorite : Icons.favorite_border))),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(property.title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 6),
                  Row(children: [const Icon(Icons.location_on_outlined, size: 18), const SizedBox(width: 4), Expanded(child: Text(property.location))]),
                  const SizedBox(height: 12),
                  Text('\$${property.price.toString()} MXN', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 12),
                  Row(children: [
                    _spec(Icons.bed_outlined, '${property.bedrooms} hab.'),
                    const SizedBox(width: 14),
                    _spec(Icons.bathtub_outlined, '${property.bathrooms} baños'),
                    const SizedBox(width: 14),
                    _spec(Icons.local_parking_outlined, '${property.parking}'),
                  ]),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _spec(IconData icon, String text) => Row(children: [Icon(icon, size: 18), const SizedBox(width: 4), Text(text)]);
}

class PropertyDetailPage extends StatefulWidget {
  final Property property;
  const PropertyDetailPage({super.key, required this.property});

  @override
  State<PropertyDetailPage> createState() => _PropertyDetailPageState();
}

class _PropertyDetailPageState extends State<PropertyDetailPage> {
  bool scheduled = false;

  @override
  Widget build(BuildContext context) {
    final p = widget.property;
    return Scaffold(
      appBar: AppBar(title: const Text('Detalle de propiedad')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(18, 8, 18, 32),
        children: [
          Container(
            height: 250,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(28),
              gradient: const LinearGradient(colors: [Color(0xFFD7C1A2), Color(0xFF8EA58F)]),
            ),
            child: const Center(child: Icon(Icons.home_work_outlined, size: 100, color: Colors.white70)),
          ),
          const SizedBox(height: 20),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(child: Text(p.title, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.w900))),
              Chip(label: Text(p.operation)),
            ],
          ),
          const SizedBox(height: 8),
          Row(children: [const Icon(Icons.location_on_outlined), const SizedBox(width: 4), Expanded(child: Text(p.location))]),
          const SizedBox(height: 14),
          Text('\$${p.price} MXN', style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w900)),
          const SizedBox(height: 22),
          Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
            _DetailSpec(icon: Icons.bed_outlined, label: '${p.bedrooms}\nHabitaciones'),
            _DetailSpec(icon: Icons.bathtub_outlined, label: '${p.bathrooms}\nBaños'),
            _DetailSpec(icon: Icons.local_parking_outlined, label: '${p.parking}\nCochera'),
          ]),
          const SizedBox(height: 24),
          const Text('Descripción', style: TextStyle(fontSize: 19, fontWeight: FontWeight.w800)),
          const SizedBox(height: 8),
          const Text('Propiedad disponible dentro del catálogo de INNOVA. Consulta sus características y agenda una visita directamente desde la aplicación móvil.', style: TextStyle(height: 1.5)),
          const SizedBox(height: 24),
          FilledButton.icon(
            onPressed: () => setState(() => scheduled = true),
            icon: const Icon(Icons.calendar_month),
            label: Text(scheduled ? 'Visita agendada' : 'Agendar visita'),
          ),
          const SizedBox(height: 10),
          OutlinedButton.icon(onPressed: () {}, icon: const Icon(Icons.person_outline), label: const Text('Ver perfil del vendedor')),
        ],
      ),
    );
  }
}

class _DetailSpec extends StatelessWidget {
  final IconData icon;
  final String label;
  const _DetailSpec({required this.icon, required this.label});
  @override
  Widget build(BuildContext context) => Column(children: [Icon(icon, size: 28), const SizedBox(height: 6), Text(label, textAlign: TextAlign.center)]);
}

class AppointmentsPage extends StatelessWidget {
  const AppointmentsPage({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const BrandedAppBar(title: 'MIS CITAS'),
      body: ListView(
        padding: const EdgeInsets.all(18),
        children: [
          const Text('Próximas visitas', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900)),
          const SizedBox(height: 16),
          _appointment('Casa Familiar Cholula', '24 septiembre · 16:30', 'Confirmada'),
          const SizedBox(height: 12),
          _appointment('Residencia La Paz', '28 septiembre · 11:00', 'Pendiente'),
          const SizedBox(height: 22),
          Card(
            color: Colors.white,
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text('¿Quieres conocer otra propiedad?', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 18)),
                const SizedBox(height: 6),
                const Text('Abre el catálogo, selecciona una propiedad y utiliza “Agendar visita”.'),
                const SizedBox(height: 12),
                FilledButton(onPressed: () {}, child: const Text('Explorar catálogo')),
              ]),
            ),
          )
        ],
      ),
    );
  }

  Widget _appointment(String property, String date, String status) {
    return Card(
      color: Colors.white,
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: const CircleAvatar(child: Icon(Icons.home_outlined)),
        title: Text(property, style: const TextStyle(fontWeight: FontWeight.w800)),
        subtitle: Padding(padding: const EdgeInsets.only(top: 4), child: Text(date)),
        trailing: Chip(label: Text(status)),
      ),
    );
  }
}

class FavoritesPage extends StatelessWidget {
  final Set<String> favorites;
  final void Function(Property) onToggleFavorite;
  const FavoritesPage({super.key, required this.favorites, required this.onToggleFavorite});

  @override
  Widget build(BuildContext context) {
    final selected = properties.where((p) => favorites.contains(p.title)).toList();
    return Scaffold(
      appBar: const BrandedAppBar(title: 'FAVORITOS'),
      body: selected.isEmpty
          ? const Center(child: Padding(padding: EdgeInsets.all(28), child: Text('Aún no tienes propiedades guardadas.\nToca el corazón de una propiedad para agregarla.', textAlign: TextAlign.center)))
          : ListView(
              padding: const EdgeInsets.all(18),
              children: selected.map((property) => Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: PropertyCard(property: property, favorite: true, onFavorite: () => onToggleFavorite(property)),
              )).toList(),
            ),
    );
  }
}
